#!/bin/bash
# Double-click this file to launch PyLearn.
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Install it from https://www.python.org/downloads/ and try again."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

# First run only: create the virtual environment and install packages
if [ ! -d "venv" ]; then
  echo "First-time setup (takes a minute)..."
  python3 -m venv venv || { echo "Could not create venv."; read -n 1 -s -r -p "Press any key..."; exit 1; }
  source venv/bin/activate
  pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt || { echo "Install failed."; read -n 1 -s -r -p "Press any key..."; exit 1; }
else
  source venv/bin/activate
fi

echo "Starting PyLearn... your browser will open shortly."
python3 -m streamlit run app.py
