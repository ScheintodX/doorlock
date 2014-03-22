#!/bin/bash

gpio -g write 7 1
sleep 3
gpio -g write 7 0
