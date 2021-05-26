#!/bin/sh

GIT_URL="https://github.com/jaraco/path"
PY="/usr/bin/python3"
LOG_FILE="log_file.log"

$PY -m venv local_lib | tee $LOG_FILE
source ./local_lib/bin/activate
$py pip --version
$py pip install git+$GIT_URL | tee -a $LOG_FILE