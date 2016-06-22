#!/usr/bin/env python

"""
	Author: Xavid Ramirez
	Email: xavidram@hotmail.com
	Purpose: Extract Station Clients from Airodump-ng
			 csv file for analysing and processing. The 
			 python script will exract the rows of Station
			 Clients and push them into a database for later
			 use. This script is for research purposes only.
"""

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

#This is the API endpoint for pushing new records into the database
API = "http://45.55.165.42/Devices/New"

def airodumpStart():
	"""
	Function: airodumpStart
	params:   NONE
	Desc: 	  airodumpStart handles the set up and execution of Airodump-ng.
			  Using the subprocess library to call subprocesses to set up the Wi-Fi
			  dongle into monitoing mode and prior to that check and kill any processes
			  that would interupt the setup or execution.
			  A couple of manually set up prinouts are executed and then using the pexpect
			  library we run airodump with a couple of arguments. We specify the interface
			  as Wlan1mon. During monitor mode set up Wlan1 which is the Wi-Fi dongle had
			  'mon' concatinated to it becoming Wlan1mon which is our interface. The output
			  format is specified as csv in the event no other files are needed but can be 
			  removed so all files are generated. '-w data' speficies to write the file out
			  to data-*.*
			  A timeout is set up on the Airodump pexpect call to set up time intervals of 
			  execution, which pexpect is then closed when the timout occurs this will write
			  the files out which can then be parsed.
	Library:  Pexpect (Better tool for controlling other applications or processes, spawn childprocesses)
			  subprocess (similar to pexpect but will call subprocesses)
	"""
	print "Setting up monitoring mode.."
	subprocess.call(["airmon-ng","check", "kill"])
	subprocess.call(["airmon-ng", "start","wlan1"])
	print "Startgin up Airodump-ng: \n\tInterface : Wlan1mon\n\tFileType: csv\n\tFilename: data-01.csv"
	cmd_airodump = pexpect.spawn('airodump-ng wlan1mon --output-format csv -w data')
	cmd_airodump.expect([pexpect.TIMEOUT, pexpect.EOF], 30)
	print "Airodump-ng Stopping...\nSaving Airodump-ng contents.."
	cmd_airodump.close()
	print "Save complete! --"

def getMAC(MACADDRESS):
	"""
		Function: getMAC
		params:   Device MAC address
		Desc:     getMAC will use the given MAC address and call the macvendors API
				  to retreive the name of the vendor of the given MAC addess. This can
				  be set up to be done by the server for a faster file processing time.
				  In the event a vendor is not found, 'Unknown' is returned.
		Libary:   urllib (open a url endpoint and return the response)
	"""
	API = 'http://api.macvendors.com/%s'
	vendor = urllib.urlopen(API % MACADDRESS).read()
	if len(vendor) > 1:
		return vendor
	else:
		return "Unkown"

def myMAC(iface):
	"""
		Function: myMAC
		Params:   Networking interface
		Desc:     A string with the name of an Interface. The function
				  will get the output of ifconfig (interface) and look for
				  the HWaddr which is the MAC address. This is used to identify
				  the node which is pushing records into the database.
		Library:  commands (execute bash/os commands)
	"""
	words = commands.getoutput("ifconfig " + iface).split()
	if "HWaddr" in words:
		return words[words.index("HWaddr") + 1]
	else:
		return 'NULL'


### Script Start ###
NodeMAC = myMAC("eth0")

#repeat this every hour until told to stop.
while True:
	print "Script starting....\n"
	print  "Script initiated at : %s" % (datetime.datetime.now())
	print "Please do not interupt the script...\n"

	airodumpStart()

	print "Processing the file... please wait."
	time.sleep(2)
	print "Pushing to database..."

	flag = 0
	file = min(glob.iglob('data-0*.csv'))	#find old data file 
	with open(file , 'rb') as csvfile:		#process file as csvfile as long as it is open and read as binary
		lines = csv.reader(csvfile)			#set up a csv file reader
		lines.next()						#skip the first null column which makes no sense as it would be line[-1] but this works
		for line in lines:					#do the following for each line in the file
			if len(line) > 1:				#make sure there is content in the line
				if "Station" in line[0]:	#keep searching until Station section is found
					flag = 1
					continue
				if flag == 1:
					payload = {'node' : NodeMAC , 'mac' : line[0] , 'firstseen': line[1] , 'lastseen' : line[2], 'company' : getMAC(line[0]) } #prepare payload
					r = requests.post(API , params=payload)	#push payload to file

	print "Successfully pushed to database"
	print "removing csv file"
	os.remove(file)		#remove current Airodump-ng file for future reinitialization
	print "Script completed at: %s" % (datetime.datetime.now())	#script end time.

