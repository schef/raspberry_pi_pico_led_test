#!/bin/bash

rshell -p /dev/ttyACM0 --buffer-size 512 cp led_blink.py /pyboard/main.py
rshell -p /dev/ttyACM0 --buffer-size 512 repl
