#!/bin/bash

# @reboot /home/pi/game/run.sh
cd /home/pi/game
find /home/pi/game/logs/ -mindepth 1 -mtime +1 -type f -delete
python3 /home/pi/game/main.py > /home/pi/game/logs/log_$(date +%s).txt 2>&1 &
exit 0
