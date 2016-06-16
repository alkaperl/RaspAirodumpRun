#!/usr/bin/env python
import os
import csv
import pexpect
import time
import subprocess
import datetime

Time = 36000

def airodumpStart():
	cmd_airodump = pexpect.spawn('airodump-ng wlan1mon -w data')
	cmd_airodump.expect([pexpect.TIMEOUT, pexpect.EOF], 10)
	cmd_airodump.close()


###ScriptStart##
#airodumpStart()

print datetime.datetime.now()