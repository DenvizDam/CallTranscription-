
import argparse
from pathlib import Path

import pandas as pd

from .engine import classify


# ============================================================
# 1. COLUMN CONFIGURATION
# ============================================================

REQUIRED = [
    "Label",
    "Transcript (AI)",
    "Transcript Threshold S2T",
    "Transcript Threshold NER",
    "Entities Extracted",
]

ADDED = [
    "RCA_Label",
    "RCA_Reason",
    "RCA_NER_Check",
    "RCA_Review",
    "RCA_Entity_Details",
]


# ============================================================
# 2. LOAD DATASET
# ============================================================

def load_dataset(input_path, sheet=0):
    src = Path(input_path)

    if not src.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dataset: {src}"
        )

    if src.suffix.lower() in (".xlsx", ".xlsm"):
        df = pd.read_excel(
            src,
            sheet_name=sheet,
            dtype=object
        )

    elif src.suffix.lower() == ".csv":
        df = pd.read_csv(
            src,
            dtype=object,
            keep_default_na=False,
            encoding="utf-8-sig"
        )

    else:
        raise ValueError(
            "Chỉ hỗ trợ input .xlsx, .xlsm hoặc .csv"
        )

    return df


# ============================================================
# 3. VALIDATE DATASET
# ============================================================

def validate_columns(df):
    missing = [
        col for col in REQUIRED
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Dataset thiếu các cột: "
            + ", ".join(missing)
        )

    collisions = [
        col for col in ADDED
        if col in df.columns
    ]

    if collisions:
        raise ValueError(
            "Các cột RCA đã tồn tại trong input: "
            + ", ".join(collisions)
        )


# ============================================================
# 4. FILTER LABEL = GOOD
# ============================================================

def filter_good_rows(df):
    """
    Chỉ giữ những dòng có Label = good.

    - Không thay đổi các cột gốc.
    - Không thay đổi giá trị Entities Extracted.
    - Giữ nguyên thứ tự các dòng được chọn.
    - Bỏ khỏi output các dòng khác good.
    """

    mask = (
        df["Label"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq("good")
        .fillna(False)
    )

    return df.loc[mask].copy()


# ============================================================
# 5. ROOT CAUSE CLASSIFICATION
# ============================================================

def classify_dataset(df):
    """
    Phân loại toàn bộ dòng đã lọc.

    Root Cause:
    - S2T
    - NER
    - Both Phase
    - No Error
    - Need Review
    """

    results = []

    for _, row in df.iterrows():

        result = classify(
            row["Transcript Threshold S2T"],
            row["Transcript Threshold NER"],
            row["Transcript (AI)"],
            row["Entities Extracted"],
            row.get("Entities To Extract")
        )

        results.append([
            result.label,
            result.reason,
            result.ner_check,
            result.review,
            result.entity_checks
        ])

    output = df.copy()

    for i, column in enumerate(ADDED):
        output[column] = [
            result[i] for result in results
        ]

    return output


# ============================================================
# 6. SAVE OUTPUT
# ============================================================

def save_output(df, output_path):
    dst = Path(output_path)

    dst.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if dst.suffix.lower() == ".xlsx":

        df.to_excel(
            dst,
            index=False
        )

    elif dst.suffix.lower() == ".csv":

        df.to_csv(
            dst,
            index=False,
            encoding="utf-8-sig"
        )

    else:
        raise ValueError(
            "Output phải là .xlsx hoặc .csv"
        )

    return dst


# ============================================================
# 7. MAIN PIPELINE
# ============================================================

def run(input_path, output_path, sheet=0):

    print("=" * 60)
    print("S2T / NER ROOT CAUSE ANALYSIS")
    print("Python Only - V6")
    print("=" * 60)

    # Step 1: Load dataset
    df = load_dataset(
        input_path,
        sheet=sheet
    )

    total_rows = len(df)

    print(f"Total input rows: {total_rows}")

    # Step 2: Validate required columns
    validate_columns(df)

    # Step 3: Filter good rows only
    df_good = filter_good_rows(df)

    good_rows = len(df_good)
    removed_rows = total_rows - good_rows

    print(f"Label = good: {good_rows}")
    print(f"Excluded rows: {removed_rows}")

    # Step 4: Classify good rows
    output = classify_dataset(df_good)

    # Step 5: Save output
    saved_path = save_output(
        output,
        output_path
    )

    print("=" * 60)
    print("CLASSIFICATION COMPLETED")
    print("=" * 60)

    print(f"Output rows: {len(output)}")
    print(f"Saved to: {saved_path}")

    print("\nROOT CAUSE DISTRIBUTION:")

    if output.empty:
        print("Không có dòng Label = good.")
    else:
        print(
            output["RCA_Label"]
            .value_counts(dropna=False)
            .to_string()
        )

    print("=" * 60)

    return output


# ============================================================
# 8. COMMAND LINE INTERFACE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "S2T / NER Root Cause Analysis "
            "- Python Only"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Đường dẫn file Excel/CSV đầu vào"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Đường dẫn file kết quả"
    )

    parser.add_argument(
        "--sheet",
        default="0",
        help="Tên sheet hoặc index sheet Excel"
    )

    args = parser.parse_args()

    sheet = (
        int(args.sheet)
        if args.sheet.isdecimal()
        else args.sheet
    )

    run(
        input_path=args.input,
        output_path=args.output,
        sheet=sheet
    )


if __name__ == "__main__":
    main()
