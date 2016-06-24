import os, subprocess

subprocess.call(["sudo" , "apt-get" , "-y" , "update"])
subprocess.call(["sudo" , "apt-get" , "-y" , "upgrade"])
subprocess.call(["sudo","apt-get","-y" ,"install" , "libssl-dev" ,"libnl-dev" , "git" , "rfkill" , "iw" , "python-pip"])
subprocess.call(["sudo" , "pip" , "install" , "pexpect"])
subprocess.call(["wget" , "http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz"])
subprocess.call(["tar", "-zxvf" , "aircrack-ng-1.2-rc4.tar.gz"])
subprocess.call(["rm" , "aircrack-ng-1.2-rc4.tar.gz"])
subprocess.call(["make", "-C" , "aircrack-ng-1.2-rc4/"])
subprocess.call(["sudo" , "make" , "install" ])
subprocess.call(["sudo" , "airodump-ng-oui-update"])
subprocess.call(["sudo","rm" , "-rf","aircrack-ng-1.2-rc4/"])

#install finished at this point.

#subprocess.call(["sudo" , "airmon-ng" , "check" , "kill"])
#subprocess.call(["sudo" , "airmon-ng" , "start" , "wlan1"])

#after this you can run airodump-ng but might want to run it with bash script at this point
