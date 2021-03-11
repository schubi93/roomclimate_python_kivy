#!/bin/bash

cd /home/pi/code/roomclimate_python_kivy/src
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
sudo timedatectl set-timezone Europe/Berlin
/usr/bin/python3 main.py