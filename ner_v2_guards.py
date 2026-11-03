"""NER V2 name-only update: precise full-name span selection; amount/term rules unchanged.

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

A. PERSON-NAME BOUNDARIES — DETERMINISTIC SELECTION ORDER (NAME KEYS ONLY):
   AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON
- OVERRIDE FOR PERSON NAMES ONLY: "take ALL tokens between the anchors" identifies a candidate REGION, not necessarily the final entity value. Never use that instruction to override an exact verified full-name match.
- FIRST: identify the correct entity key and candidate region using the question pattern and nearby anchors. Do not use hints intended for other person-name keys.
- SECOND: read the FULL name hint belonging to this exact key, if present. A hint is corroborating evidence, never permission to insert a missing name.
- THIRD (HIGHEST PRIORITY WHEN SUPPORTED): if the full hinted name occurs as a COMPLETE, CONTIGUOUS TOKEN SEQUENCE inside the candidate region of normalized_transcript (case-insensitive, accents must match), extract THAT MATCHING SEQUENCE and no adjacent words. Compare word boundaries, not substring characters. Preserve the spelling/case in normalized_transcript. Do this even if the region contains an extra repeated spoken token immediately before it.
- FOURTH: if the hint does not match transcript, do not manufacture its value. Use utterance evidence to locate the true boundaries; where ambiguous, do not guess that a repeated syllable is extra.
- IMPORTANT CONTRASTIVE EXAMPLE (illustrative, NOT a fixed customer name): transcript "Bên mua bảo hiểm là Mai Trần Thị Ngọc Mai, sinh năm ..." + trusted POLICYOWNER hint "Trần Thị Ngọc Mai" => POLICYOWNER "Trần Thị Ngọc Mai" (NOT "Mai Trần Thị Ngọc Mai"). normalized_transcript retains every spoken token.
- COUNTEREXAMPLE: transcript "Bên mua bảo hiểm là Nguyễn Thị Ngọc Mai" + full-name hint "Nguyễn Thị Ngọc Mai" => preserve ALL four name tokens. Do not drop a prefix just to shorten names; repeated or familiar words alone are not sufficient evidence of disfluency.
- Never output a name from reference/hints that does not appear in normalized_transcript. Never alter any non-person-name entity, the original dictionary, or the output schema.

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
1. PERSON-NAMES: if this exact key has a trusted full-name hint that matches a complete contiguous sequence of words INSIDE its candidate region in normalized_transcript, return that exact span only; do NOT include an adjacent repeated token or title. Recheck that every word in output is in the matched transcript span, and that the hint is not being used for another key. Without evidence, preserve genuine multiword names and do not guess. Keep normalized_transcript unchanged.
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
