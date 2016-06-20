#!/usr/bin/env python
import os
import csv
import pexpect
import time
import datetime
import requests
import json
import commands
import urllib
import subprocess
import glob

url = "http://45.55.165.42/Device"

def airodumpStart():
	print "Setting up monitoring mode.."
	subprocess.call(["airmon-ng","check", "kill"])
	subprocess.call(["airmon-ng", "start","wlan1"])
	print "Startgin up Airodump-ng:"
	print "\tInterface : Wlan1mon"
	print "\tFileType: csv"
	print "\tFilename: data-01.csv"
	cmd_airodump = pexpect.spawn('airodump-ng wlan1mon --output-format csv -w data')
	cmd_airodump.expect([pexpect.TIMEOUT, pexpect.EOF], 30)
	print "Airodump-ng Stopping..."
	print "Saving Airodump-ng contents.."
	cmd_airodump.close()
	print "Save complete! --"

def getMAC(MACADDRESS):
	#one api   http://searchmac.com/api/raw/
	#second api   http://macvendors.co/api/
	#third option http://api.macvendors.com/
	API = 'http://api.macvendors.com/%s'
	vendor = urllib.urlopen(API % MACADDRESS).read()
	if len(vendor) > 1:
		return vendor
	else:
		return "Unkown"

def myMAC(iface):
	words = commands.getoutput("ifconfig" + iface).split()
	if "HWaddr" in words:
		return words[words.index("HWaddr") + 1]
	else:
		return 'NULL'

###ScriptStart##
#airodumpStart()

while True:
	print "Script starting....\n"

	print  "Script initiated at : %s" % (datetime.datetime.now())
	print "Please do not interupt the script...\n"

	airodumpStart()

	print "Processing the file... please wait."
	time.sleep(2)
	print "Pushing to database..."

	file = min(glob.iglob('data-0*.csv'))
	with open(file , 'rb') as csvfile:
		lines = csv.reader(csvfile)
		lines.next()
		for line in lines:
			if len(line) > 1:
				if "Station" in line[0]:
					lines.next()
					for line in lines:
						if len(line) > 1:
							payload = {'node' : myMac("etho") , 'mac' : line[0] , 'firstseen': line[1] , 'lastseen' : line[2], 'company' : getMAC(line[0]) }
							r = requests.post(url , params=payload)

	print "Successfully pushed to database"
	print "removing csv file"
	os.remove(file)
	print "Script completed at: %s" % (datetime.datetime.now())
	
