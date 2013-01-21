#!/bin/bash

if [ $(ps aux | grep 'pnartadjadjnvadv' | grep 'python' | wc -l | tr -s "\n") -eq 0 ]
then
    cd /home/acooke/webapps/colorlessgreen
    source env/bin/activate
    PYTHONPATH=src nohup python src/pnartadjadjnvadv/process.py >> /home/acooke/logs/user/colorlessgreen.log 2>&1 &
fi

