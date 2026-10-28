"""Extra prompt guidance for S2T V3. No reference/masking logic modification."""

ACOUSTIC = '''
<entity_audio_accuracy_v3>
ENTITY ACCURACY (STEP 1: LISTEN TO AUDIO):
- Follow all original REFERENCE rules as written; do not change their meaning.
- FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT: carefully distinguish each spoken
  numeral (hundreds/tens/units), the quantity scale (nghìn/triệu/tỷ), and
  the currency unit. Never replace "bảy trăm năm mươi" with "ba trăm năm mươi"
  merely because the latter sounds more common.
- Do not add an unspoken monetary scale word such as "nghìn", "triệu",
  or "tỷ" to make a colloquial amount sound more natural.
  If audio says "mười triệu bốn trăm đồng", transcribe those words,
  not "mười triệu bốn trăm nghìn đồng".
- AGENTCODE, PROPOSALNO, REFERENCENO: identify each audible letter and digit
  in order, including repeated digits and leading zeros. Never complete a
  partial code using expected length or business patterns.
- CELLPHONE, PHONENUMBER: transcribe spoken digits as ordered identifiers,
  including repeated zeros. Do not force a typical phone-number length.
- AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON: preserve names actually
  spoken. Apply existing proper-name/reference spelling rules without
  changing the person's identity or inventing missing syllables.
- PREMIUMTERM: preserve the spoken duration and its unit (năm/tháng/ngày).
  PREMIUMMODE: preserve the spoken payment frequency. These are distinct;
  do not infer either from the other.
- If an entity value is unclear in audio, do not invent missing components.
- These are recognition guides, NOT output entity fields or new JSON keys.
</entity_audio_accuracy_v3>
'''

NORMALIZATION = '''
<entity_normalization_integrity_v3>
ENTITY INTEGRITY (STEP 2: FORMAT ONLY):
- Converting spoken words to written numerals must preserve the Step 1 value.
- FACEAMOUNT, TOTALPREMIUM, SUNDRYAMOUNT: preserve number magnitude and unit.
  "bảy trăm năm mươi triệu" -> "750 triệu"; NEVER "350 triệu".
- Do not insert, remove, or infer any scale word ("nghìn", "triệu",
  "tỷ") while formatting amounts. A missing scale word must not be
  filled in from convention or expected business magnitude.
- "mười triệu bốn trăm đồng" -> "10 triệu 400 đồng";
  NEVER "10 triệu 400 nghìn đồng".
- AGENTCODE, PROPOSALNO, REFERENCENO: preserve each spoken letter/digit,
  sequence, repeated digit, and leading zero. Do not add omitted characters.
- CELLPHONE, PHONENUMBER: preserve digit order and leading zeros; treat as
  strings, not numeric quantities. Do not guess a missing area/prefix digit.
- AGENTNAME, POLICYOWNER, INSUREDNAME, CONTACTPERSON: capitalization or
  permissible spelling correction must not change the person's identity.
- PREMIUMTERM: keep the spoken duration and unit. PREMIUMMODE: preserve
  payment frequency; do not conflate it with the duration of the policy.
- Step 2 must not silently replace a Step 1 amount/code/phone/term with a
  different value; do not fill absent values.
- All original normalization and REFERENCE instructions remain authoritative.
</entity_normalization_integrity_v3>
'''

SELF_CHECK = '''
<entity_consistency_self_check_v3>
BEFORE RETURNING THE EXISTING JSON FORMAT:
- Compare step1_raw and transcript at matching text positions.
- Every clearly recognized monetary amount must have an equivalent value
  and unit across the two fields.
- Compare explicit scale words ("nghìn", "triệu", "tỷ") separately:
  Step 2 must not add an unspoken scale word, even if the result seems
  more natural or typical for an insurance payment.
- For "10 triệu 400 đồng" in step1_raw, reject "10 triệu 400 nghìn đồng"
  in transcript and restore the Step 1-supported phrase.
- Each phone/code/proposal/reference identifier must preserve exact letters,
  digits, order, repeated characters, and leading zeros.
- Names must preserve the same speaker-intended identity; durations must keep
  the same number and unit; payment frequencies must not be changed.
- If Step 2 altered a value without support from Step 1, restore its
  Step 1-derived representation.
- This checks normalization consistency only. It does not prove that Step 1
  correctly heard the audio. Follow all original REFERENCE rules unchanged.
</entity_consistency_self_check_v3>
'''


def insert_v3_guards(template: str) -> str:
    """Insert exactly once into existing sections without editing other text."""
    for tag, block, sentinel in (
        ('</step_1_raw_transcription>', ACOUSTIC, '<entity_audio_accuracy_v3>'),
        ('</step_2_normalization>', NORMALIZATION, '<entity_normalization_integrity_v3>'),
        ('</self_check>', SELF_CHECK, '<entity_consistency_self_check_v3>'),
    ):
        if sentinel in template:
            continue
        if template.count(tag) != 1:
            raise ValueError(f'Expected one {tag}; found {template.count(tag)}. No changes made.')
        template = template.replace(tag, block + '\n' + tag, 1)
    return template
