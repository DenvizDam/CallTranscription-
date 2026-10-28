"""NER V2 update: generic name-boundary guards and existing amount/term format rules.

No values, keys, metadata, reference masking, or JSON schema are changed here.
The guards are inserted outside the original reference block.
"""

NORMALIZATION_GUARD = """
<ner_v2_normalization_guard>
ENTITY FORMAT SAFETY (applies to normalized_transcript):
- Preserve the meaning and value of every number in the input transcript. Never infer missing digits or monetary scale words.
- Keep the existing normalization rules for the transcript. IMPORTANT: output-format rules below apply to extracted entity values, NOT to normalized_transcript itself.
- A spoken amount such as "280 triệu đồng" may remain "280 triệu đồng" in normalized_transcript; only the extracted monetary entity becomes "280000000".
- Do not modify names, entities, or reference text to make them match a hint or expected script.
</ner_v2_normalization_guard>
"""

EXTRACTION_GUARD = """
<ner_v2_entity_extraction_guard>
HIGH-PRIORITY ENTITY OUTPUT RULES (only for keys in the existing Step 2 entity list):

A. PERSON-NAME BOUNDARIES AND SPOKEN SELF-CORRECTIONS:
   AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON
- Find the person's name span in normalized_transcript; do not simply take every token after an anchor such as "là" or "tên là".
- Spoken speech may include a false start, an isolated repeated name token, an address term, or a self-correction immediately before the complete name. Such extra speech is NOT part of the extracted name when supported by context.
- Compare plausible contiguous candidate spans against the surrounding utterance, reference/question role, and any reliable case-specific name hint. A hint may HELP CHOOSE between spans present in the transcript; it must NEVER introduce a name absent from the transcript.
- When a single token immediately before a complete name appears to be a false start (for example, a call-out of the final given-name token followed by a full name), and the shorter complete-name span is corroborated by the utterance or reliable hint, omit the false-start token from the entity. Preserve that token in normalized_transcript.
- IMPORTANT: repeating a token or having a common Vietnamese family name is only a CLUE, not proof. A genuine four-/five-word name must be preserved intact. Do not remove a token solely to produce a three-word name, and do not hardcode any person-specific name.
- Choose the narrowest FULL name span adequately supported by evidence, not the shortest possible span. Do not omit meaningful middle names or append unrelated neighboring words.
- If evidence cannot distinguish the proposed name boundaries, do not claim certainty or invent a corrected name; follow the original extraction policy for ambiguous values.

B. MONEY: FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT
- Output a STRING of digits representing the full integer amount in VND, with no spaces, thousands separators, decimal marks, or unit words.
- "280 triệu đồng" -> "280000000"; "10 triệu 400 đồng" -> "10000400" (NOT "10400000").
- Preserve exactly the monetary scale words present in normalized_transcript; do NOT insert "nghìn", "triệu", or "tỷ" by expectation.
- If the value cannot be determined unambiguously from the transcript, output "" instead of inventing a number.

C. PREMIUMTERM
- Output only the numeric duration as a STRING of digits; remove the trailing time unit from the extracted VALUE, not from normalized_transcript.
- "20 năm" -> "20" (NOT "20 năm").
- Do not convert months to years or infer a duration. If the transcript's duration is ambiguous, output "".
- Do not apply this rule to PREMIUMMODE or any other key.

All other existing entity extraction rules remain in force.
</ner_v2_entity_extraction_guard>
"""

SELF_CHECK_GUARD = """
<ner_v2_output_self_check>
Before producing the final JSON, check only keys actually required in Step 2:
1. PERSON-NAMES: assess whether a token before a complete name is a speech false start, repeated call-out, or a genuine name component. Cross-check surrounding context, question role, and any reliable case-specific hint. Exclude extra tokens only with supporting evidence. Keep normalized_transcript unchanged; never fabricate a name or truncate a genuine multiword name.
2. FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT: each nonempty output must match ^[0-9]+$ and equal the monetary value expressed in normalized_transcript.
3. PREMIUMTERM: each nonempty output must match ^[0-9]+$, with no "năm", "tháng", spaces, or punctuation; its digits must come from the transcript.
4. Preserve the exact set of entity keys; do not create extra keys and do not fill absent evidence from hints or reference.
5. Keep normalized_transcript and output JSON schema exactly as previously specified.
</ner_v2_output_self_check>
"""


def enhance_prompt(prompt: str) -> str:
    """Insert each guard once into a fully formatted NER prompt.

    Raise on unexpected templates to avoid silently returning an unenhanced prompt.
    """
    if "<ner_v2_normalization_guard>" in prompt:
        return prompt
    substitutions = (
        ("</step_1_normalization>", NORMALIZATION_GUARD),
        ("</step_2_extraction>", EXTRACTION_GUARD),
        ("</self_check>", SELF_CHECK_GUARD),
    )
    for closing_tag, addition in substitutions:
        if prompt.count(closing_tag) != 1:
            raise ValueError(f"Expected one {closing_tag} in NER prompt; found {prompt.count(closing_tag)}")
        prompt = prompt.replace(closing_tag, addition + "\n" + closing_tag, 1)
    return prompt
