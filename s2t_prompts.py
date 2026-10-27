"""V3 S2T prompts; replacement module; requires original renamed to s2t_prompts_original.py.

Caller keeps its existing import: from s2t_prompts import get_prompt
Original get_prompt() code, reference masking and dictionary are reused verbatim.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import FunctionType

from s2t_v3_guards import insert_v3_guards

source_file = Path(__file__).resolve().with_name('s2t_prompts_original.py')
if not source_file.is_file():
    raise FileNotFoundError(f'Missing original backup s2t_prompts_original.py: {source_file}')
spec = importlib.util.spec_from_file_location('_original_s2t_prompt_v3', source_file)
if spec is None or spec.loader is None:
    raise ImportError(f'Cannot load original module: {source_file}')
_original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_original)

# No change to original dictionary, entities, metadata, or original module.
dictionary = _original.dictionary
TRANSCRIPTION_WITH_NORMALIZATION = insert_v3_guards(_original.TRANSCRIPTION_WITH_NORMALIZATION)
BASIC_TRANSCRIPTION = insert_v3_guards(_original.BASIC_TRANSCRIPTION)

# Execute the EXACT original get_prompt function bytecode with only the two
# template globals replaced. Reference construction and masking are untouched.
_v3_globals = dict(_original.get_prompt.__globals__)
_v3_globals.update(
    TRANSCRIPTION_WITH_NORMALIZATION=TRANSCRIPTION_WITH_NORMALIZATION,
    BASIC_TRANSCRIPTION=BASIC_TRANSCRIPTION,
)
get_prompt = FunctionType(
    _original.get_prompt.__code__,
    _v3_globals,
    name=_original.get_prompt.__name__,
    argdefs=_original.get_prompt.__defaults__,
    closure=_original.get_prompt.__closure__,
)
get_prompt.__kwdefaults__ = _original.get_prompt.__kwdefaults__
get_prompt.__annotations__ = dict(_original.get_prompt.__annotations__)
get_prompt.__doc__ = _original.get_prompt.__doc__

__all__ = ['dictionary', 'TRANSCRIPTION_WITH_NORMALIZATION',
           'BASIC_TRANSCRIPTION', 'get_prompt']
