import base64
import urllib2
import time
import datetime
from threading import Thread


record = open("/DNS.html", "w", 0)
record.write(str(datetime.datetime.now()) + "  Loading module...\r\n")
record.close()
def MaoLog(logString):
	record = open("/DNS.html", "a", 0)
	record.write(logString + "\r\n")
	record.close()

def update_IP():
	while True:
		try:
			request = urllib2.Request("http://ip.chinaz.com/getip.aspx")
			response = urllib2.urlopen(url=request, timeout=5)
		except:
			MaoLog(str(datetime.datetime.now()) + "  Net ip error!")
			time.sleep(5)
		else:
			if(response.getcode() == 200):
				try:
					global ipRet
					ipRet = response.read().split(',')[0].split(':')[1].split("'")[1]
					MaoLog(str(datetime.datetime.now()) + "  Get public ip: " + ipRet)
					time.sleep(50)
				except:
					global ipRet
					ipRet = ""
					MaoLog(str(datetime.datetime.now()) + "  Parse ip error!")
					time.sleep(5)
			else:
				time.sleep(5)

def update_DNS():
	while (ipRet == ""):
		time.sleep(3)
	
	while True:
		uri = "http://ddns.oray.com/ph/update?hostname=maojianwei.wicp.net&myip=" + ipRet
		request = urllib2.Request(uri)
		request.add_header("Authorization","Basic bWFvamlhbndlaTo2bTZhNW80NzEyMQ==")
		request.add_header("User-Agent","Oray")

		try:
			response = urllib2.urlopen(url=request, timeout=5)
			# urllib2.urlopen(request)
			MaoLog(str(datetime.datetime.now()) + "   *  " + str(response.getcode()) + " " + response.read())
			time.sleep(100)
		except:
			MaoLog(str(datetime.datetime.now()) + "  Tell DNS error!")
			time.sleep(5)

ipRet = ""
def main():
	MaoLog(str(datetime.datetime.now()) + "  Init tracking threads...")
	updateIP = Thread(target=update_IP)
	updateIP.start()
	updateDNS = Thread(target=update_DNS)
	updateDNS.start()
	MaoLog(str(datetime.datetime.now()) + "  Auto tracking...")

if __name__ == "__main__":
	main()
