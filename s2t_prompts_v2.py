"""S2T prompt V2 – standalone companion module to existing s2t_prompts.py.

Keep the original s2t_prompts.py UNCHANGED in the same directory.
Place this module beside it as s2t_prompts_v2.py.
To use the new prompts, update the caller import to refer to s2t_prompts_v2.
No dictionary or entity key is renamed.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
from typing import Dict, Optional

# Load original module to preserve all existing dictionary entries verbatim.
_ORIGINAL_PATH = Path(__file__).resolve().with_name("s2t_prompts.py")
if not _ORIGINAL_PATH.exists():
    raise FileNotFoundError(
        "Missing original s2t_prompts.py in the same folder as s2t_prompts_v2.py."
    )
_spec = importlib.util.spec_from_file_location("_s2t_prompts_source_for_v2", _ORIGINAL_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load original S2T module: {_ORIGINAL_PATH}")
_original = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_original)

# Preserve exact dictionary keys, values, all I3/C2 scripts and entity names.
dictionary = _original.dictionary

# Strictly bounded changes: add entity guards inside existing prompt sections.
ENTITY_ACOUSTIC_GUARD = """
<entity_acoustic_guard>
AUDIO-ONLY EVIDENCE FOR ENTITY VALUES:
- Do not guess or copy any value from REFERENCE, a script or business expectation.
- Monetary values (FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT): attend to each
  audible numerical syllable, its order and its unit (nghìn/triệu/tỷ/đồng).
  "bảy trăm năm mươi triệu" and "ba trăm năm mươi triệu" are different.
- Identifiers (AGENTCODE, PROPOSALNO, REFERENCENO): capture each spoken letter
  and digit in order, including leading/repeated zeros. Never auto-complete.
- Phone numbers (CELLPHONE, PHONENUMBER): hear individual digit sequences,
  not numeric quantities. Preserve all audible digits and zeros.
- Names (AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON): preserve spoken
  identity and syllables; reference names are not proof that they were said.
- Durations (PREMIUMTERM): preserve number and spoken unit (năm/tháng/ngày),
  distinguish from a date and from frequency (PREMIUMMODE).
- The rules above apply to any related fields; the identifiers named above
  are examples from the EXISTING dictionary, not new fields or output keys.
- Never add missing syllables, digits, names or units. Preserve negation.
</entity_acoustic_guard>
"""

ENTITY_NORMALIZATION_GUARD = """
<entity_normalization_guard>
ENTITY VALUE PRESERVATION DURING STEP 2:
- Only change written representation; never change what was spoken in step1_raw.
- Amounts (FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT): preserve the exact
  mathematical amount and monetary unit; "bảy trăm năm mươi triệu đồng"
  may become "750 triệu đồng" but NEVER "350 triệu đồng".
  Keep existing unit-word format (tỷ, triệu, nghìn, đồng).
- Codes (AGENTCODE, PROPOSALNO, REFERENCENO): combine ONLY heard letters/digits
  in order; preserve leading and repeated zeros; no inferred prefix/suffix.
  "E A không một hai" -> "EA012"; "E A không không năm" -> "EA005".
- Phone (CELLPHONE, PHONENUMBER): convert uttered digits into a digit string,
  keeping initial zeros, repeated digits and exact order. Do not enforce length.
- Names: capitalization/spelling adjustment must not substitute a different
  person's name. Existing strict proper-noun repair rules still apply in
  TRANSCRIPTION_WITH_NORMALIZATION; BASIC_TRANSCRIPTION gains no reference
  name-repair permission.
- Duration (PREMIUMTERM): preserve number and unit; "mười lăm năm" ->
  "15 năm", not "15 tháng" or "1 năm". Do not confuse with PREMIUMMODE.
- Maintain all existing negation, accent, brand, filler and output rules.
- REFERENCE is NEVER a source for a missing monetary amount, phone digit,
  agent code, proposal number or other actual spoken value.
</entity_normalization_guard>
"""

ENTITY_CROSS_STEP_CHECK = """
<entity_cross_step_check>
FINAL CHECK BEFORE JSON:
- For each identifiable value in step1_raw, match its counterpart in transcript
  in the same order. Confirm amount value/unit; duration value/unit; exact
  digits and letters of code/phone; same spoken identity for personal names.
- Restore the step1_raw-derived value if Step 2 changed a value accidentally.
- Do not guess or use REFERENCE to repair a possible Step 1 hearing error.
- This self-check verifies consistency, NOT acoustic correctness; Step 1
  mistakes require audio-based review or retranscription.
</entity_cross_step_check>
"""


def _add_guard(template: str, closing_tag: str, guard: str) -> str:
    """Insert once immediately before the section's closing tag."""
    if template.count(closing_tag) != 1:
        raise ValueError(f"Expected exactly one {closing_tag}, got {template.count(closing_tag)}")
    if guard.strip() in template:
        return template
    return template.replace(closing_tag, guard + "\n" + closing_tag, 1)


def _optimize_template(template: str) -> str:
    for tag, extra in (
        ("</step_1_raw_transcription>", ENTITY_ACOUSTIC_GUARD),
        ("</step_2_normalization>", ENTITY_NORMALIZATION_GUARD),
        ("</self_check>", ENTITY_CROSS_STEP_CHECK),
    ):
        template = _add_guard(template, tag, extra)
    return template


TRANSCRIPTION_WITH_NORMALIZATION = _optimize_template(
    _original.TRANSCRIPTION_WITH_NORMALIZATION
)
BASIC_TRANSCRIPTION = _optimize_template(_original.BASIC_TRANSCRIPTION)


def get_prompt(
    prompt_type: str = "TRANSCRIPTION_WITH_NORMALIZATION",
    metadata: Optional[Dict] = None,
) -> str:
    """Return same formatted prompt interface as original; add no new fields."""
    prompt_mapping = {
        "BASIC_TRANSCRIPTION": BASIC_TRANSCRIPTION,
        "TRANSCRIPTION_WITH_NORMALIZATION": TRANSCRIPTION_WITH_NORMALIZATION,
    }
    base_prompt = prompt_mapping.get(prompt_type, TRANSCRIPTION_WITH_NORMALIZATION)
    if metadata:
        script_version = metadata.get("script_version", "")
        question_no = metadata.get("question_no", "")
        textscript = metadata.get("textscript", "")
        parameter = metadata.get("parameter", "")
        if textscript:
            # Preserve original reference-digit masking logic verbatim.
            textscript = re.sub(r"\d", "x", textscript)
    else:
        script_version = question_no = textscript = parameter = ""
    return base_prompt.format(
        script_version=script_version,
        question_no=question_no,
        textscript=textscript,
        parameter=parameter,
    )


__all__ = [
    "dictionary", "TRANSCRIPTION_WITH_NORMALIZATION", "BASIC_TRANSCRIPTION",
    "get_prompt",
]
