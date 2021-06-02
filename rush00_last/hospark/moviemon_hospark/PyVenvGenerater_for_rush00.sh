#!/bin/bash

TEXT="
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#      = Python V.env Generater =                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42seoul.kr>           +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#             Be Enjoy! :)                             #+#    #+#              #
#                                                     ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
"

DJ_PATH_NAME="./rush00_venv"
PY="/usr/bin/python3"
LOG_FILE="log_file.log"

$PY -m venv $DJ_PATH_NAME | tee $LOG_FILE

source $DJ_PATH_NAME/bin/activate

echo "$TEXT"

python -m pip --version

pip install --upgrade pip | tee -a $LOG_FILE
python -m pip install --force-reinstall -r requirement.txt | tee -a $LOG_FILE
source $DJ_PATH_NAME/bin/activate


