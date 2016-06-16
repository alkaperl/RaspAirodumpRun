#!/usr/bin/env python
import os, csv, pexpect,time
from poormanslogging import info, warn, error

import src.settings as settings

Time = 36000

def airodumpStart():
	cmd_airodump = pexpect.spawn('airodump-ng wlan1mon -w data')
	cmd_airodump.expect([pexpect.TIMEOUT, pexpect.EOF], 10)
	cmd_airodump.close()


airodumpStart()