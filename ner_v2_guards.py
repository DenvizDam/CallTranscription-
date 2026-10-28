"""NER V2: prompt-only guards for confirmed boundary and format errors.

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

A. PERSON-NAME BOUNDARIES: AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON
- Extract the actual person's name; do not include an introductory form of address, repeated call-out, or unrelated word before the name.
- When a reliable expected-name hint EXACTLY matches a contiguous name span already present in normalized_transcript, prefer that span over a longer span containing extra words. A hint must NEVER create a name absent from the transcript.
- Example for a case with a verified hint of "Nguyễn Quốc Khánh":
  transcript "bên mua bảo hiểm là Khánh Nguyễn Quốc Khánh" -> POLICYOWNER = "Nguyễn Quốc Khánh" (not "Khánh Nguyễn Quốc Khánh").
- However, do NOT unconditionally delete the first word or force Vietnamese names to three words. Without reliable span evidence, do not guess the boundary.

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
1. PERSON-NAMES: exclude extra address/call-out tokens when the exact intended name span is supported by the normalized transcript and boundary evidence. Never fabricate or truncate a genuine multiword name.
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
