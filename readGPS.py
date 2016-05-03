import serial
import time
import datetime


def main():

    dateTime = ""
    latitude = ""
    longitude = ""
    satellite = ""

    print "start"
    
    ser = serial.Serial("/dev/ttyAMA0", 9600)

    while(True):
        resultGPS = ""
        while(True):
            if(0 != ser.inWaiting()):
                resultGPS += ser.read()
                if("\n" == resultGPS[-1]):
                    break
            else:
                time.sleep(1)

        resultGPS = resultGPS.split(",")
        if(len(resultGPS)>1):
            if('$GPGGA' == resultGPS[0] and len(resultGPS) > 8):
                if(resultGPS[2] != ""):
                    temp = str(float(resultGPS[2])/100).split(".")
                    latitude = str(float(temp[0]) + float("0." + temp[1])/0.6)
                    print "***********"
                    print temp
                else:
                    latitude = "lost"

                if (resultGPS[4] != ""):
                    temp = str(float(resultGPS[4]) / 100).split(".")
                    longitude = str(float(temp[0]) + float("0." + temp[1])/0.6)
                    print "***********"
                    print temp
                else:
                    longitude = "lost"

                satellite = resultGPS[7]

                print "-------------------"
                print (resultGPS)
                print latitude + "," + longitude + "," + satellite

            elif('$GPZDA' == resultGPS[0] and len(resultGPS) > 6):
                dateTime = datetime.datetime(int(resultGPS[4]),
                                             int(resultGPS[3]),
                                             int(resultGPS[2]),
                                             int(resultGPS[1][0:2]),
                                             int(resultGPS[1][2:4]),
                                             int(resultGPS[1][4:6]))
                print "-------------------"
                print (resultGPS)
                print dateTime
            else:
                pass

main()
