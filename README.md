ls -lah /media/project_165/speechtotext/testset/data_PRD

python build_failed_case_testset.py \
  --excel "./20261008_db_analysis_Q3_2026.xlsx" \
  --data-root "/media/project_165/speechtotext/testset/data_PRD" \
  --output "./failed_case_testset" \
  --sheet "DB Records" \
  --dry-run


  python build_failed_case_testset.py \
  --excel "./20261008_db_analysis_Q3_2026.xlsx" \
  --data-root "/media/project_165/speechtotext/testset/data_PRD" \
  --output "./failed_case_testset" \
  --sheet "DB Records"
