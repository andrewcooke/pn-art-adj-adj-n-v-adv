#!/bin/bash

cd /home/acooke/webapps/colorlessgreen
source env/bin/activate
PYTHONPATH=src nohup python src/pnartadjadjnvadv/process.py &
