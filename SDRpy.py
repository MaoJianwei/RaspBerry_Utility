
import time
import os

run = False

while(True):
	
	if(False == run):
		os.system("sudo /home/pi/MaoSystem/SDR.sh")
		run = True

	time.sleep(3600)