@echo off
set PYTHONUNBUFFERED=1
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
echo Starting VectorVault at http://127.0.0.1:8000 ...
python -m app.main
