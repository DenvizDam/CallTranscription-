"""Compatible NER prompt wrapper: precise name-boundary conflict fix only.

Keep the original implementation in ner_prompts_original.py, and keep the
existing ner_v2_guards.py unchanged. This wrapper preserves get_prompt API,
metadata handling, dictionaries, and the original formatted prompt, except
for two conflicting PERSON-NAME instructions in <step_2_extraction>.
"""
from typing import Dict, Optional
import importlib
import re

try:
    from .ner_v2_guards import enhance_prompt
except ImportError:
    from ner_v2_guards import enhance_prompt

_original = importlib.import_module(__package__ + ".ner_prompts_original" if __package__ else "ner_prompts_original")

dictionary = _original.dictionary
NER_EXTRACTION_PROMPT_WITH_POSITION = _original.NER_EXTRACTION_PROMPT_WITH_POSITION

# The new rule only changes PERSON-NAME entity span selection. It does not
# modify normalization, text/reference/hints, monetary formatting, term
# formatting, JSON keys, or any other extraction instruction.
_NAME_BOUNDARY_REPLACEMENT = """  * PERSON-NAME CANDIDATE REGION VS. EXACT NAME SPAN (OVERRIDES ONLY OLD PERSON-NAME SPAN-LENGTH RULES):
    Use the context anchors in the pattern to locate a CANDIDATE REGION. The entire region is NOT automatically the final entity value.
    A kinship word may be part of a genuine name; do not remove any word merely because it is repeated, common, or looks like a title.
    For each person-name key (AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON), consult only its own reliable, case-specific full-name hint.
    If that full hinted name appears as one contiguous, complete word sequence within the candidate region of normalized_transcript (case-insensitive; Vietnamese diacritics must match), select exactly that transcript span, with no adjacent extra token. Do not copy words from hints/reference into the output.
    Example: candidate region 'Bách Nguyễn Thế Bách'; reliable POLICYOWNER hint 'Nguyễn Thế Bách'; choose 'Nguyễn Thế Bách', not 'Bách Nguyễn Thế Bách'. The extra first 'Bách' remains in normalized_transcript.
    Counterexample: candidate region 'Nguyễn Thị Ngọc Mai'; hint 'Nguyễn Thị Ngọc Mai'; keep the complete four-word name. Never automatically prefer a longer name or cut a first word simply to make the name shorter.
    If the hint is absent, does not match the actual transcript, or contradicts the utterance, use transcript evidence and the question context; do not fabricate a name or force a hint match.
"""

_PERSON_HEADER = re.compile(r"(?m)^\s*-\s*PERSON-NAME BOUNDARIES\s*\(")
_NEXT_HEADER = re.compile(r"(?m)^\s*-\s*NUMERIC CODES\s*\(")
_OLD_SPAN_BULLET = re.compile(r"(?im)^\s*\*\s*BUT a kinship word CAN be a real name syllable\.")
_OLD_TIE_BULLET = re.compile(r"(?im)^\s*\*\s*Tie-break by hint word count:")


def _fix_name_conflict(prompt: str) -> str:
    """Rewrite just the two old person-name bullets, not the original file.

    Fail closed if the source template no longer has the expected structure,
    rather than silently claiming the fix was applied.
    """
    if "PERSON-NAME CANDIDATE REGION VS. EXACT NAME SPAN (OVERRIDES" in prompt:
        return prompt
    headers = list(_PERSON_HEADER.finditer(prompt))
    if len(headers) != 1:
        raise ValueError("Expected exactly one PERSON-NAME BOUNDARIES section in NER prompt")
    start = headers[0].end()
    tail = _NEXT_HEADER.search(prompt, start)
    if tail is None:
        raise ValueError("Cannot locate NUMERIC CODES section after PERSON-NAME BOUNDARIES")
    before, section, after = prompt[:start], prompt[start:tail.start()], prompt[tail.start():]
    old_span = _OLD_SPAN_BULLET.search(section)
    old_tie = _OLD_TIE_BULLET.search(section)
    if not old_span or not old_tie or old_span.start() >= old_tie.start():
        raise ValueError("Original PERSON-NAME span / tie-break bullets changed; review before patching")
    # Preserve the original pronoun/title exclusion rule above the old bullets.
    # Replace only the two old person-name bullets and any example text between
    # them; no non-name section or metadata is changed.
    prefix = section[:old_span.start()].rstrip()
    replacement = "\n" + _NAME_BOUNDARY_REPLACEMENT.rstrip() + "\n"
    return before + prefix + replacement + after


def _build_prompt(text: str) -> str:
    # The optional WITH_POSITION prompt was empty in the supplied screenshots;
    # preserve unsupported / empty templates as the original implementation did.
    if "<step_1_normalization>" not in text:
        return text
    corrected = _fix_name_conflict(text)
    return enhance_prompt(corrected)


NER_EXTRACTION_PROMPT = _build_prompt(_original.NER_EXTRACTION_PROMPT)


def get_prompt(
    prompt_type: str = "NER_EXTRACTION_PROMPT",
    transcript: str = "",
    metadata: Optional[Dict] = None,
) -> str:
    """Use the original formatter; modify ONLY conflicting name instructions."""
    text = _original.get_prompt(
        prompt_type=prompt_type, transcript=transcript, metadata=metadata
    )
    return _build_prompt(text)
