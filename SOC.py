import urllib2
import json
import sqlite3


def getPage(pageNo): # output (result, json)

	print "\tGet Page..."

	result = True

	url = "http://www.soc.aero/misc/flightlist.php?page=" + str(pageNo) + "&Company=&Pilot=&AircraftID=&Craft=&From=&To=&Status=&Time="

	headers = {'User-Agent':'MaoJianwei/2.1 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) BigMao2012/20091201 BUPT/0.6.0'}
	

	getData = None

	try:
		req = urllib2.Request(url = url, headers = headers)
		
		response = urllib2.urlopen(req,timeout = 10)

		getData = response.read()

	except Exception,e:
		result = False
		print "\t",Exception,":",e
		print "\tGet Page Fail..."

	return (result, getData)

def recordSQL(dbConnect, dataJson):

	print "Recording Flight ..."

	cursor = dbConnect.cursor()

	try:

		dataObj = json.loads(dataJson)
		dataObj = dataObj["list"]

		for i in range(0,20):
			if("2" == dataObj[i][10]):
				query ='INSERT INTO FlightListSOC VALUES (' \
					+ dataObj[i][0] + ','\
					'"'+ dataObj[i][1] + '",'\
					'"'+ dataObj[i][2] + '",'\
					'"'+ dataObj[i][3] + '",'\
					'"'+ dataObj[i][4] + '",'\
					'"'+ dataObj[i][5] + '",'\
					'"'+ dataObj[i][11] + '",'\
					'"'+ dataObj[i][12] + '",'\
					'"'+ dataObj[i][6] + '",'\
					'"'+ dataObj[i][7] + '",'\
					'"'+ dataObj[i][8] + '",'\
					'"'+ dataObj[i][9] + '"'\
					+ ')'

				try:
					cursor.execute(query)
					dbConnect.commit()
				except Exception,e:
					print Exception,":",e

		print "Recording Flight OK !"

	except Exception,e:
		print "Recording Flight Fail..."
		print Exception,"out for:",e

	cursor.close();

	


def initSQL(): # output dbCursor

	print "Open Init Database..."

	#flightDB = sqlite3.connect("d:/MaoFlightSOC.db")
	flightDB = sqlite3.connect("/home/pi/MaoFlightSOC.db")
	cursor = flightDB.cursor()

	try:
		cursor.execute("CREATE TABLE FlightListSOC ("
		"TaskNo INT primary key not null unique,"
		"FlightNo text,"
		"DeliverDate text,"
		"DepICAO text,"
		"ArrICAO text,"
		"PlaneModel text,"
		"PlaneName text,"
		"Pilot text,"
		"Passenger text,"
		"Score text,"
		"Reputation text,"
		"Income text"
		")")
	except Exception,e:
		print Exception,":",e

	cursor.close()

	return flightDB




def main():



	db = initSQL()

	i = 1
	while(i<=2200):
		print "----- Start Page " + str(i) + " -----"

		(ret, json) = getPage(i)

		if(True == ret):
			recordSQL(dbConnect = db, dataJson = json)
			i = i + 1

	db.close()



if __name__ == "__main__":

	main()