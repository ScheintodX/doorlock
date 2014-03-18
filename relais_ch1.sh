#!/bin/bash

gpio -g mode 7 out

if [ $1 == "an" ]
then
	gpio -g write 7 1
else
	gpio -g write 7 0
fi
