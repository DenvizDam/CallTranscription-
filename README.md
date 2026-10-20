conda create -n s2t_rca python=3.11 -y

conda activate s2t_rca

python -m pip install -r requirements.txt
python -m pip install -e .




3. Chạy chương trình
Chạy Python Rules:
python -m rootcause.cli \
  --input input/dataset.xlsx \
  --output output/result.xlsx


Chạy Python kết hợp LLM:
python -m rootcause.cli \
  --input input/dataset.xlsx \
  --output output/result_llm.xlsx \
  --llm
