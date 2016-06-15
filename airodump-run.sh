#!/bin/bash
# airodumpCont
#
# This tool requires aircrack-ng tools to be installed and run as root
#
# ChangeLog....
VERSION="1.0"
# Version 1.0 - First Release

#################################################################
# CHECKING FOR ROOT
#################################################################
if [ `echo -n $USER` != "root" ]
then
	echo "MESSAGE:"
	echo "MESSAGE: ERROR: Please run as root!"
	echo "MESSAGE:"
	exit 1
fi

#################################################################
# CHECKING TO SEE IF INTERFACE IS PROVIDED
#################################################################
if [ -z ${1} ]
then
	echo "MESSAGE: Version number ${VERSION}"
	echo "MESSAGE: Usage: `basename ${0}` [interface] [BSSID] [channel]"
	echo "MESSAGE: Example #`basename ${0}` wlan0 (everything else is optional)"
	exit 1
else
	INTERFACE="`echo "${1}" | cut -c 1-6`"
	echo "MESSAGE: Putting ${INTERFACE} in monitor mode"
fi

#################################################################
# PUT WIFI IN MONITOR MODE
#################################################################
airmon-ng check kill #check and kill any processes that may intterupt
airmon-ng start ${INTERFACE}
#new interface name
INTERFACE = "wlan1mon"
iwconfig ${INTERFACE} # mon0

#################################################################
# GET INTERFACE MAC ADDRESS
#################################################################
MACADDRESS=`ifconfig ${INTERFACE} | grep ${INTERFACE} | tr -s ' ' | cut -d ' ' -f5 | cut -c 1-17`

#################################################################
# Get current time , script will run at hourly intervals
#################################################################

#################################################################
# START AIRODUMP IN XTERM WINDOW
#################################################################
echo "MESSAGE: Starting packet capture - Ctrl-c to end it"
airodump-ng wlan1 -w node1
sleep 2

TIME = $(date + "%s")
END = $(date + "%s") + 60
while [$TIME -ne END]
do
	TIME = $(date + "%s")
done


#################################################################
# Stopping program
#################################################################
kill ${AIREPLAYPID}
airmon-ng stop ${INTERFACE}
exit 0