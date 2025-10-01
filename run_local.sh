#!/usr/bin/env bash
set -euo pipefail

python src/collector.py
python src/structurer.py
python src/loader.py
streamlit run app/streamlit_app.py --server.port 8501

