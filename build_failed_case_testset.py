#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a failed-case WAV + decoded-metadata test set from an Excel DB Records sheet.

No third-party packages required. Runs on Windows or Linux, provided all input
paths are accessible from the machine executing this script.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL_DOC = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL_PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'x': MAIN}
QID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
AUDIO_RE = re.compile(r'^qid_([0-9a-f-]{36})\.wav$', re.I)
PAYLOAD_RE = re.compile(r'^qid_([0-9a-f-]{36})_corrid_(.+)\.json$', re.I)
REPORT_FIELDS = ['QID', 'Source_Rows', 'Audio_Count', 'Payload_Count', 'Audio_Path',
                 'Payload_Path', 'Metadata_Valid', 'Status', 'Details', 'Output_Folder']
LOG = logging.getLogger('failed-case-testset')


def qid_normalize(value: object) -> str | None:
    text = str(value).strip().lower() if value is not None else ''
    return text if QID_RE.fullmatch(text) else None


def _get_sheet_path(z: zipfile.ZipFile, sheet_name: str) -> str:
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    sheets = wb.find(f'{{{MAIN}}}sheets')
    selected = None
    for sheet in sheets or []:
        if sheet.get('name') == sheet_name:
            selected = sheet
            break
    if selected is None:
        raise ValueError(f'Sheet {sheet_name!r} not found in workbook')
    rel_id = selected.get(f'{{{REL_DOC}}}id')
    rel_root = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    target = next((r.get('Target') for r in rel_root if r.get('Id') == rel_id), None)
    if not target:
        raise ValueError(f'Worksheet relationship not found: {rel_id}')
    import posixpath
    if target.startswith('/'):
        path = target.lstrip('/')
    else:
        path = posixpath.normpath(posixpath.join('xl', target))
    if path not in z.namelist():
        raise ValueError(f'Worksheet XML is missing: {path}')
    return path


def _shared_strings(z: zipfile.ZipFile) -> list[str]:
    if 'xl/sharedStrings.xml' not in z.namelist():
        return []
    values: list[str] = []
    with z.open('xl/sharedStrings.xml') as stream:
        for _, elem in ET.iterparse(stream, events=('end',)):
            if elem.tag == f'{{{MAIN}}}si':
                values.append(''.join(t.text or '' for t in elem.iter(f'{{{MAIN}}}t')))
                elem.clear()
    return values


def _column_index(cell_ref: str) -> int:
    letters = re.match(r'[A-Z]+', cell_ref.upper())
    if not letters:
        raise ValueError(f'Invalid Excel cell address: {cell_ref!r}')
    idx = 0
    for letter in letters.group(0):
        idx = idx * 26 + (ord(letter) - ord('A') + 1)
    return idx - 1


def _cell_value(cell: ET.Element, shared: list[str]) -> str:
    typ = cell.get('t')
    if typ == 'inlineStr':
        return ''.join(n.text or '' for n in cell.iter(f'{{{MAIN}}}t'))
    v = cell.find(f'{{{MAIN}}}v')
    raw = '' if v is None or v.text is None else v.text
    if typ == 's' and raw:
        try:
            return shared[int(raw)]
        except (IndexError, ValueError) as e:
            raise ValueError(f'Invalid shared-string index: {raw}') from e
    return raw


def read_excel_qids(path: Path, sheet: str) -> tuple[dict[str, list[int]], dict[str, int]]:
    """Read .xlsx without external dependencies; respects cell VALUES, not Excel UI filters."""
    if not path.is_file():
        raise FileNotFoundError(f'Excel not found: {path}')
    selected: dict[str, list[int]] = defaultdict(list)
    counts = {'data_rows': 0, 'matching_rows': 0, 'invalid_qid_rows': 0}
    with zipfile.ZipFile(path) as z:
        shared = _shared_strings(z)
        xml_path = _get_sheet_path(z, sheet)
        header = None
        columns = {}
        with z.open(xml_path) as stream:
            for _, element in ET.iterparse(stream, events=('end',)):
                if element.tag != f'{{{MAIN}}}row':
                    continue
                row_id = int(element.get('r', '0'))
                cells = {}
                for c in element.findall(f'{{{MAIN}}}c'):
                    ref = c.get('r', '')
                    if ref:
                        cells[_column_index(ref)] = _cell_value(c, shared).strip()
                if header is None:
                    # Header identified by the three required column names; not just fixed row index.
                    found = {v.strip().lower(): col for col, v in cells.items()}
                    if all(k in found for k in ('qid', 'quality', 'label')):
                        header = row_id
                        columns = {k: found[k] for k in ('qid', 'quality', 'label')}
                elif row_id > header:
                    counts['data_rows'] += 1
                    quality = cells.get(columns['quality'], '').strip()
                    label = cells.get(columns['label'], '').strip()
                    if quality == 'Non-Perfect' and label == 'good':
                        counts['matching_rows'] += 1
                        qid = qid_normalize(cells.get(columns['qid'], ''))
                        if qid:
                            selected[qid].append(row_id)
                        else:
                            counts['invalid_qid_rows'] += 1
                            LOG.warning('Invalid or empty QID at Excel row %s', row_id)
                element.clear()
        if header is None:
            raise ValueError('Could not find QID, Quality, Label headers in DB Records sheet')
    return dict(selected), counts


def index_files(root: Path, kind: str, desired: set[str]) -> dict[str, list[Path]]:
    if not root.is_dir():
        raise NotADirectoryError(f'Missing directory: {root}')
    regexp = AUDIO_RE if kind == 'audio' else PAYLOAD_RE
    suffix = '.wav' if kind == 'audio' else '.json'
    found: dict[str, list[Path]] = defaultdict(list)
    visited = 0
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() != suffix:
            continue
        visited += 1
        match = regexp.fullmatch(path.name)
        if match:
            qid = qid_normalize(match.group(1))
            if qid and qid in desired:
                found[qid].append(path)
    LOG.info('Indexed %s %s file(s), matched %s QID(s)', visited, kind, len(found))
    return dict(found)


def decode_metadata(payload_path: Path) -> dict:
    try:
        with payload_path.open('r', encoding='utf-8-sig') as f:
            payload = json.load(f)
    except (OSError, UnicodeError, json.JSONDecodeError) as e:
        raise ValueError(f'Cannot parse payload JSON: {e}') from e
    if not isinstance(payload, dict) or 'metadata' not in payload:
        raise ValueError('Payload must be a JSON object containing metadata')
    value = payload['metadata']
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f'Metadata JSON string is invalid: {e}') from e
    if not isinstance(value, dict):
        raise ValueError('Decoded metadata must be a JSON object')
    if 'Keywords' not in value or not isinstance(value['Keywords'], list):
        raise ValueError('Decoded metadata must contain Keywords as an array')
    return value


def write_report(rows: list[dict], dest: Path, summary: dict) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    report_path = dest / 'matching_report.csv'
    with report_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with (dest / 'summary.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    LOG.info('Report: %s', report_path)


def build(excel: Path, data_root: Path, output: Path, sheet: str, dry_run: bool) -> int:
    audio_root = data_root / 'audios'
    payload_root = data_root / 'payloads'
    if not audio_root.is_dir() or not payload_root.is_dir():
        raise FileNotFoundError('Both data_PRD/audios and data_PRD/payloads must exist')
    excel = excel.resolve()
    data_root = data_root.resolve()
    output = output.resolve()
    if output == data_root or data_root in output.parents:
        raise ValueError('Output must NOT be inside data_PRD (protect original dataset)')
    if output in (excel.parent, audio_root, payload_root):
        raise ValueError('Unsafe output directory')

    qid_rows, counts = read_excel_qids(excel, sheet)
    LOG.info('Filtered %s matching row(s) -> %s unique valid QID(s)', counts['matching_rows'], len(qid_rows))
    audio_index = index_files(audio_root, 'audio', set(qid_rows))
    payload_index = index_files(payload_root, 'payload', set(qid_rows))
    results = []
    totals = defaultdict(int)
    cases_root = output / 'cases'
    # Old layout would mix per-QID directories with the new flat files.
    if not dry_run and cases_root.is_dir() and any(p.is_dir() for p in cases_root.iterdir()):
        raise ValueError("Output cases/ contains subdirectories from the old layout. "
                         "Use a new --output path, e.g. ./failed_case_testset_flat.")

    for qid, excel_rows in sorted(qid_rows.items()):
        audios = sorted(audio_index.get(qid, []), key=str)
        payloads = sorted(payload_index.get(qid, []), key=str)
        row = {
            'QID': qid, 'Source_Rows': ','.join(map(str, excel_rows)),
            'Audio_Count': len(audios), 'Payload_Count': len(payloads),
            'Audio_Path': ' | '.join(map(str, audios)),
            'Payload_Path': ' | '.join(map(str, payloads)),
            'Metadata_Valid': '', 'Status': '', 'Details': '', 'Output_Folder': '',
        }
        if not audios and not payloads:
            status = 'MISSING_BOTH'
        elif not audios:
            status = 'MISSING_AUDIO'
        elif not payloads:
            status = 'MISSING_PAYLOAD'
        elif len(audios) > 1 or len(payloads) > 1:
            status = 'DUPLICATE_FILES'
        else:
            status = 'READY'

        meta = None
        if status == 'READY':
            try:
                meta = decode_metadata(payloads[0])
                row['Metadata_Valid'] = 'Yes'
            except ValueError as exc:
                status = 'INVALID_METADATA'
                row['Metadata_Valid'] = 'No'
                row['Details'] = str(exc)
        if status == 'READY':
            # Flat layout: every matching QID has two sibling files, QID.wav + QID.json.
            wav_dest = cases_root / f'{qid}.wav'
            json_dest = cases_root / f'{qid}.json'
            row['Output_Folder'] = str(cases_root)
            if dry_run:
                status = 'DRY_RUN_READY'
            elif wav_dest.exists() or json_dest.exists():
                status = 'ALREADY_EXISTS'
                row['Details'] = 'At least one output file exists; pair not overwritten.'
            else:
                cases_root.mkdir(parents=True, exist_ok=True)
                # Stage files with unique names inside destination folder before publishing.
                token = uuid.uuid4().hex
                wav_tmp = cases_root / f'.{qid}.{token}.wav.tmp'
                json_tmp = cases_root / f'.{qid}.{token}.json.tmp'
                published_wav = False
                try:
                    shutil.copy2(audios[0], wav_tmp)
                    with json_tmp.open('w', encoding='utf-8') as f:
                        json.dump(meta, f, ensure_ascii=False, indent=2)
                        f.write('\n')
                    # Avoid touching pre-existing output files.
                    if wav_dest.exists() or json_dest.exists():
                        status = 'ALREADY_EXISTS'
                        row['Details'] = 'Output was created concurrently; pair not overwritten.'
                    else:
                        wav_tmp.rename(wav_dest)
                        published_wav = True
                        json_tmp.rename(json_dest)
                        status = 'COMPLETE'
                except Exception:
                    if published_wav:
                        wav_dest.unlink(missing_ok=True)
                    raise
                finally:
                    wav_tmp.unlink(missing_ok=True)
                    json_tmp.unlink(missing_ok=True)
        row['Status'] = status
        totals[status] += 1
        results.append(row)

    summary = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'excel': str(excel), 'sheet': sheet,
        'data_root': str(data_root), 'output': str(output),
        'filter': {'Quality': 'Non-Perfect', 'Label': 'good'},
        'excel_counts': counts, 'unique_valid_qids': len(qid_rows),
        'result_status_counts': dict(totals),
        'notes': 'matching_report.csv is UTF-8 BOM and can be opened in Excel. Original source files are unchanged.',
    }
    write_report(results, output, summary)
    LOG.info('DONE: %s', json.dumps(summary['result_status_counts'], ensure_ascii=False))
    # Non-zero return warns about incomplete matching, but report is always saved.
    failures = sum(n for status, n in totals.items() if status not in ('COMPLETE', 'DRY_RUN_READY', 'ALREADY_EXISTS'))
    return 2 if failures else 0


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Build WAV/metadata JSON pairs for filtered failed cases.')
    parser.add_argument('--excel', type=Path, default=script_dir / '20261008_db_analysis_Q3_2026.xlsx')
    parser.add_argument('--data-root', type=Path, default=script_dir / 'data_PRD')
    parser.add_argument('--output', type=Path, default=script_dir / 'failed_case_testset_flat')
    parser.add_argument('--sheet', default='DB Records')
    parser.add_argument('--dry-run', action='store_true', help='Match and validate, but do not copy WAV/JSON cases.')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(levelname)s | %(message)s')
    try:
        return build(args.excel, args.data_root, args.output, args.sheet, args.dry_run)
    except Exception as exc:
        LOG.error('%s: %s', type(exc).__name__, exc)
        if args.verbose:
            LOG.exception('Traceback')
        return 1


if __name__ == '__main__':
    sys.exit(main())
