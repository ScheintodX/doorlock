#!/bin/bash
number=$RANDOM
echo $number
cd /home/pi/python-qrcode/scripts/
sudo ./qr https://192.168.0.23:443?c=$number$number$number$number
