#!/bin/bash

sh /home/pi/game/stop.sh || true
cp main.py game.py electro.py audio.py field.py run.sh stop.sh reboot.sh /home/pi/game/
chmod +x /home/pi/game/run.sh
chmod +x /home/pi/game/stop.sh
chmod +x /home/pi/game/reboot.sh
