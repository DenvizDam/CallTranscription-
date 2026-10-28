"""NER V2 update: case-specific full-name hint priority, plus existing amount/term rules.

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

A. PERSON-NAME BOUNDARIES, HINT PRIORITY, AND SPOKEN SELF-CORRECTIONS:
   AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON
- PRIORITY OVERRIDE FOR PERSON-NAME SPANS: The old pattern instruction to "take ALL tokens between the anchors" locates a candidate region, NOT the final name boundary. For PERSON-NAME entities only, apply the rules in this section AFTER locating that region. Do not blindly include every intervening token.
- First find all complete contiguous name candidates actually present in normalized_transcript. Never construct a name from reference or hint text when it does not occur in the transcript.
- If a reliable case-specific hint for the current person-name key contains a FULL person name and that FULL name appears as one contiguous word sequence in normalized_transcript (case-insensitive; preserve Vietnamese diacritics), prefer exactly the matching name span over a longer anchor-based span that includes immediately adjacent extra words. Output the casing/spelling from normalized_transcript after the permitted normalization, not a copied hint. The expected hint MUST NOT introduce any absent word.
- Example of boundary selection ONLY (not a name to memorize): transcript "là Mai Trần Thị Ngọc Mai, sinh năm ..." and verified hint "Trần Thị Ngọc Mai" -> POLICYOWNER "Trần Thị Ngọc Mai"; keep the initial "Mai" in normalized_transcript. Apply the same logic to every person name; do not hardcode any particular name.
- Recognize spoken false starts, isolated repeated given-name words, and self-corrections before a complete name, but only omit them when a reliable hint or sufficiently explicit utterance supports the shorter COMPLETE name. A token that happens to repeat is NOT automatically disfluency.
- A verified FULL name of four or five words stays intact. Do NOT use a three-word limit, a Vietnamese surname list, or the shortest possible span as a substitute for evidence.
- If the hint is missing, vague, conflicting, or not present in normalized_transcript, do not force a hint-based correction. Use context and the original extraction rules; do not invent or truncate a name.
- This priority override changes only the final PERSON-NAME entity value. Do NOT delete, rewrite, or remove extra speech from normalized_transcript, and do not affect other entity keys.

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
1. PERSON-NAMES: the anchor-to-anchor region is a candidate ONLY; if a reliable full-name hint occurs contiguously in normalized_transcript, output exactly that full matched span rather than surrounding extra words. If no such evidence exists, preserve genuine multiword names and avoid guessing. Keep normalized_transcript unchanged.
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
