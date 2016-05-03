#coding=utf-8

import sqlite3
import socket
import fcntl
import struct
# import os
import datetime

# Windows:
# localIP = socket.gethostbyname(socket.gethostname())
# print "local ip:%s "%localIP

# ipList = socket.gethostbyname_ex(socket.gethostname())
# for i in ipList:
#     if i != localIP:
#        print "external IP:%s"%i 


# Linux:
def get_ip_address(NetworkAdapterName):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', NetworkAdapterName[:15])
    )[20:24])



def main():

	# os.system("sudo python -m SimpleHTTPServer 80 &")

	IP = get_ip_address("eth0")
	# IP = "10.205.14.14"
	PORT = str(5511)
	count = 1


	dlnaDB = sqlite3.connect("/var/lib/minidlna/files.db")
	# dlnaDB = sqlite3.connect("E:\\minidlnaDB\\files.db")
	dlnaDBunit = dlnaDB.cursor()

	dlnaDBunit.execute("select * from DETAILS")
	result = dlnaDBunit.fetchall()

	html = open("/index.html", "w", 0)
	# html = open("E:\\minidlnaDB\\index.html", "w", 0)
	html.write(("<html><head><base target=\"_blank\"/><title>BigMao Radio Station</title></head><body><h1>" + u"MaoJianwei 媒体资源站" + "</h1></br>" + u"页面更新时间：" + str(datetime.datetime.now()) + "</br></br>").encode("gbk"))

	for record in result:
		if(None != record[1]):
			if("." == record[1][-3] or
				"." == record[1][-4] or
				"." == record[1][-5]):

				dot = record[1].rfind(".")
				slash1 = record[1].rfind("/") + 1
				slash2 = record[1].rfind("\\") + 1
				

				fileID = str(record[0])
				fileType = record[1][dot+1:].encode("gbk")
				fileUrl = ("http://" + IP + ":" + PORT + "/MediaItems/" + fileID + "." + fileType).encode("gbk")
				fileName = None
				if(slash1 > 0):
					fileName = record[1][slash1:dot].encode("gbk")
				else:
					fileName = record[1][slash2:dot].encode("gbk")


				fileHTML = (str(count) + ".\t<a href=" + fileUrl+ ">" + fileName + "</a></br>")#.encode("gbk")
				count = count + 1

				html.write(fileHTML)


	html.write("</body></html>")
	html.close()
	



if __name__ == '__main__':
	main()