"""NER V2 overlay: leave ner_prompts.py (V1) unchanged.

Usage: place this file and ner_v2_guards.py alongside the original ner_prompts.py.
Switch imports in the caller to ner_prompts_v2 to use V2.

For deployments that must keep `from ner_prompts import get_prompt`, rename original
ner_prompts.py to ner_prompts_original.py and rename this module to ner_prompts.py;
then change ORIGINAL_MODULE below to 'ner_prompts_original'.
"""
from typing import Dict, Optional
import importlib

from ner_v2_guards import enhance_prompt

ORIGINAL_MODULE = "ner_prompts_original"
_original = importlib.import_module(ORIGINAL_MODULE)

# Re-export original data. Actual contents are always sourced from the user's code.
dictionary = _original.dictionary
NER_EXTRACTION_PROMPT = enhance_prompt(_original.NER_EXTRACTION_PROMPT)
NER_EXTRACTION_PROMPT_WITH_POSITION = _original.NER_EXTRACTION_PROMPT_WITH_POSITION


def get_prompt(
    prompt_type: str = "NER_EXTRACTION_PROMPT",
    transcript: str = "",
    metadata: Optional[Dict] = None,
) -> str:
    """Delegate to unmodified V1 formatter, then add V2 rules to the final prompt."""
    text = _original.get_prompt(prompt_type=prompt_type, transcript=transcript, metadata=metadata)
    # The optional WITH_POSITION prompt in the screenshots is empty. Preserve it.
    if "<step_1_normalization>" not in text:
        return text
    return enhance_prompt(text)
