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
API = "http://45.55.165.42/Request/newRecord"

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
				payload = {'node' : NodeMAC , 'mac' : line[0] , 'firstseen': line[1] , 'lastseen' : line[2]} #prepare payload
				r = requests.post(API , params=payload)	#push payload to file
				if 200 != r.status_code:
					with open('errorLog.txt' , 'a') as errorLog:
						errorLog.write(r.text)

print "removing csv file"
os.remove(file)		#remove current Airodump-ng file for future reinitialization