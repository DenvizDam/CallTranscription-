

python -m py_compile ner_prompts.py ner_prompts_original.py ner_v2_guards.py



python -c "import ner_prompts; print('NER V2:', callable(ner_prompts.get_prompt))"
