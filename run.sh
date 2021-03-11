#! /bin/sh

# @reboot /home/pi/run.sh
cd /home/pi
python3 /home/pi/main.py &
exit 0
