#!/bin/bash

nohup python3 zectrix_hot.py > /var/log/zectrix_hot.log 2>&1 &

echo "zectrix_hot.py 已启动，PID: $!"