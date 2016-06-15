#!/usr/bin/env python
import time
import pexpect
import fcntl
import os
import sys

Time = 36000

def airodumpStart():
	threading.Timer(Time, airodumpStart).start()
	airodump = pexpect.spawn('airodump-ng wlan1mon -w data') 
    time.sleep(10)
    airodump.close()


airodumpStart()