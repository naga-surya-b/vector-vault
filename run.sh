#!/usr/bin/env bash
set -e
python3 -m venv .venv || true
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
echo "Starting VectorVault at http://127.0.0.1:8000 ..."
python -m app.main
