#!/bin/sh

GIT_URL="https://github.com/jaraco/path"
PY="/usr/bin/python3"
LOG_FILE="log_file.log"

$PY -m venv local_lib | tee $LOG_FILE

source ./local_lib/bin/activate

echo "\n\n== Welcome! ==\n\n"
python -m pip --version | tee -a $LOG_FILE
echo "\n\n"
python -m pip install --force-reinstall git+$GIT_URL | tee -a $LOG_FILE

python my_program.py
