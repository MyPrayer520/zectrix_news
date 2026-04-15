#!/bin/bash

pkill -f "python3 zectrix_hot.py"
sleep 1
nohup python3 zectrix_hot.py > /var/log/zectrix_hot.log 2>&1 &

echo "zectrix_hot.py 已重启，PID: $!"