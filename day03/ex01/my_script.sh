#!/bin/sh

GIT_URL="https://github.com/jaraco/path"
PY="/usr/bin/python3"
LOG_FILE="log_file.log"

$PY -m venv local_lib
source ./local_lib/bin/activate