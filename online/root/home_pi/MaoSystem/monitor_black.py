import re
import subprocess
# import commands
import socket
import fcntl
import struct
import time
# import serial
import datetime
# import urllib
# import os
# import thread
import sys

# ----- 5110 LCD -----
# import Adafruit_Nokia_LCD as LCD
# import Adafruit_GPIO.SPI as SPI
# import Image
# import ImageDraw
# import ImageFont
# ----- 5110 LCD -----



# Windows:
# localIP = socket.gethostbyname(socket.gethostname())
# print "local ip:%s "%localIP

# ipList = socket.gethostbyname_ex(socket.gethostname())
# for i in ipList:
#     if i != localIP:
#        print "external IP:%s"%i 

My_Number = ""


# Linux:
def get_ip_address(NetworkAdapterName):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', NetworkAdapterName[:15])
    )[20:24])

def find_all_mask():    # just linux
    ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    maskstr = '0x([0-9a-f]{8})'

    ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
    output = ipconfig_process.stdout.read()
    mask_pattern = re.compile('(netmask %s)' % maskstr)
    pattern = re.compile(maskstr)

    mask_pattern = re.compile(r'Mask:%s' % ipstr)
    pattern = re.compile(ipstr)
    masklist = []
    for maskaddr in mask_pattern.finditer(str(output)):
        mask = pattern.search(maskaddr.group())
        if mask.group() != '0xff000000' and mask.group() != '255.0.0.0':
            masklist.append(mask.group())

    if(len(masklist) < 1):
        return "1.0.8.0"

    return masklist[0]

# def get_cpu_temp():
#     tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
#     cpu_temp = tempFile.read()
#     tempFile.close()
#     return float(cpu_temp)/1000
#     # Uncomment the next line if you want the temp in Fahrenheit
#     #return float(1.8*cpu_temp)+32

# def get_gpu_temp():
#     gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
#     return  float(gpu_temp)
#     # Uncomment the next line if you want the temp in Fahrenheit
#     # return float(1.8* gpu_temp)+32


def MaoChangeIP01(ip_string):
    newString = ""

    for s in ip_string:
        if ("0" == s):
            newString = newString + "1"
        else:
            newString = newString + "0"

    return newString

def MaoGetIpBroad():

    IP_mask_str = find_all_mask()
    if("1.0.8.0" == IP_mask_str):
        return ("7.1.8.1", "1.0.8.0")

    IP_mask_num = struct.unpack("!L", socket.inet_aton(find_all_mask()))[0]
    IP_mask_num = int(MaoChangeIP01(bin(IP_mask_num)[2:]),2)

    try:
        IP_num = struct.unpack("!L", socket.inet_aton(get_ip_address("eth0")))[0]

        # Broadcast_num = IP_mask_num | IP_num

        Broadcast = socket.inet_ntoa(struct.pack('!L', (IP_mask_num | IP_num)))
        IP = get_ip_address("eth0")
    except:
        IP = "7.1.8.1"
        Broadcast = "1.0.8.0"

    return (IP, Broadcast)


# def soundIP(doIP):
#     cmd = 'espeak -ven+f3 -k5 -s100 "Hello, this is Big Mao Server node ' + My_Number + '"'
#     os.system(cmd)
#     IPpiece = doIP.split('.')
#
#     for piece in IPpiece:
#         os.system("espeak -ven+f3 -k5 -s100 ." + piece)
#
#     return


def BroadcastToMasterLAN(MasterBroadcastLAN, FROM, TO, sock, msg):
    for i in range(FROM, TO):
        sock.sendto(msg, (MasterBroadcastLAN + str(i), 7181))


# def getEnvironmentTemp(devicePath):
#     temperature = ""
#     try:
#         tempFile = open(devicePath)
#         tempText = tempFile.read()
#         tempFile.close()
#
#         if(type(tempText) == str):
#             tempText = tempText.split("\n")
#
#             if (len(tempText) == 3):
#                 tempText = tempText[1].split("=")
#
#                 if (len(tempText) == 2):
#                     temperature = str(float(tempText[1]) / 1000)
#                 else:
#                     temperature = "Data Format unable"
#             else:
#                 temperature = "Data Format unable"
#         else:
#             temperature = "Data Format unable"
#     except:
#         temperature = "Device unable"
#
#     return temperature


# dateTime = "init"
# latitude = "init"
# longitude = "init"
# satellite = "init"
# def workGPS(nullStr):
#
#     global dateTime, latitude, longitude, satellite
#
#     ser = serial.Serial("/dev/ttyAMA0", 9600)
#
#     while (True):
#         resultGPS = ""
#         while (True):
#             if (0 != ser.inWaiting()):
#                 resultGPS += ser.read()
#                 if ("\n" == resultGPS[-1]):
#                     break
#             else:
#                 time.sleep(1)
#
#         resultGPS = resultGPS.split(",")
#         if (len(resultGPS) > 1):
#             if ('$GPGGA' == resultGPS[0] and len(resultGPS) > 8):
#
#                 if (resultGPS[2] != ""):
#                     temp = str(float(resultGPS[2]) / 100).split(".")
#                     latitude = str(float(temp[0]) + float("0." + temp[1]) / 0.6)
#                     if(len(latitude)>10):
#                         latitude = latitude[:10]
#                 else:
#                     latitude = "lost"
#
#                 if (resultGPS[4] != ""):
#                     temp = str(float(resultGPS[4]) / 100).split(".")
#                     longitude = str(float(temp[0]) + float("0." + temp[1]) / 0.6)
#                     if (len(longitude) > 11):
#                         longitude = longitude[:11]
#                 else:
#                     longitude = "lost"
#
#                 if(resultGPS[7] != ""):
#                     satellite = resultGPS[7]
#                 else:
#                     satellite = "lost" # in reality, can not go here
#
#             elif ('$GPZDA' == resultGPS[0] and len(resultGPS) > 6):
#                 if(resultGPS[1] != "" and resultGPS[2] != "" and resultGPS[3] != "" and resultGPS[4] != ""):
#
#                     dateTime = datetime.datetime(int(resultGPS[4]),
#                                                  int(resultGPS[3]),
#                                                  int(resultGPS[2]),
#                                                  int(resultGPS[1][0:2]),
#                                                  int(resultGPS[1][2:4]),
#                                                  int(resultGPS[1][4:6]))
#                 else:
#                     dateTime = datetime.datetime(1970,1,1,0,0,0) # lost is "1970-01-01 00:00:00"
#             else:
#                 pass
#
#
#
# DC = 25
# RST = 22
# SPI_PORT = 0
# SPI_DEVICE = 0
#
# First_Line = -2
# Line = 6
# def getNewImage():
#     image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
#     draw = ImageDraw.Draw(image)
#     draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
#     addOneLine(draw, "Mao Cloud v0.6", 0, True)
#     return (image, draw)
#
# def addOneLine(draw, txt, lineNum, isInit=False):
#     font = ImageFont.truetype('/home/pi/MaoSystem/5110.ttf', 10)
#     if(isInit):
#         draw.text((0, First_Line), txt, font=font)
#     else:
#         draw.text((0, First_Line + (lineNum + 1) * Line), txt, font=font)
#     return
#
# def clearLCD(screen):
#     screen.clear()
#     screen.display()
#     return
#
# def showLCD(screen, image):
#     screen.image(image)
#     screen.display()
#     return
#
# def getCharWidth(char):
#     if(char == '1'):
#         return 2+1
#     elif(char == 'i' or char == 'I'):
#         return 1+1
#     elif(char == ';' or char == ',' or char == '.'):
#         return 1+1
#     elif(char == '\n'):
#         return 0
#     else:
#         return 5+1
#
# def showStringNew(screen, text):
#
#     (image, draw) = getNewImage()
#
#     lineCounter = 1
#     charCounter = 0
#
#     subLen = 0
#     subStr = ""
#     while(charCounter < len(text)):
#         charLen = getCharWidth(text[charCounter])
#         if(charLen == 0):
#             addOneLine(draw, subStr, lineCounter)
#             charCounter = charCounter + 1
#             lineCounter = lineCounter + 1
#             subLen = 0
#             subStr = ""
#         elif(subLen + charLen > 84):
#             addOneLine(draw, subStr, lineCounter)
#             lineCounter = lineCounter + 1
#             subLen = 0
#             subStr = ""
#         else:
#             subStr = subStr + text[charCounter]
#             subLen = subLen + charLen
#             charCounter = charCounter + 1
#
#     addOneLine(draw, subStr, lineCounter)
#     showLCD(screen, image)
#     return
#
# def initLCD():
#     screen = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
#     screen.begin(contrast=60)
#     clearLCD(screen)
#     return screen
#
#
#
# def workLCD(nullStr):
#
#     global IP, CPU_Temp, GPU_Temp, Count, SysTime, Env_Temp
#     global GPS_Lat, GPS_Lon, GPS_Satellite, GPS_Time
#
#
#     screen = initLCD()
#
#     while(True):
#
#         show = "IP: " + IP + "\nCount: " + Count + "\nCPU-T: " + CPU_Temp + "\nGPU-T: " + GPU_Temp + "\nEnv-T: " + Env_Temp + "\n" + SysTime.split(" ")[0]
#         showStringNew(screen, show)
#         time.sleep(3)
#
#         show = "IP: " + IP + "\nCount: " + Count + "\nCPU-T: " + CPU_Temp + "\nGPU-T: " + GPU_Temp + "\nEnv-T: " + Env_Temp + "\n" + SysTime.split(" ")[1]
#         showStringNew(screen, show)
#         time.sleep(3)
#
#         show = "IP: " + IP + "\nLat:" + GPS_Lat + "\nLon:" + GPS_Lon + "\nSat:" + GPS_Satellite + "\n" + GPS_Time.split(" ")[0] + "\n" + GPS_Time.split(" ")[1]
#         showStringNew(screen, show)
#         time.sleep(6)



IP = ""
CPU_Temp = ""
GPU_Temp = ""
Count = ""
SysTime = ""
GPS_Lat = ""
GPS_Lon = ""
GPS_Satellite = ""
GPS_Time = ""
Env_Temp = ""
NodeName = ""
def main():

    # thread.start_new_thread(workGPS, ("",))
    # thread.start_new_thread(workLCD, ("",))

    # global dateTime, latitude, longitude, satellite
    global IP, CPU_Temp, GPU_Temp, Count, SysTime, Env_Temp, NodeName
    global GPS_Lat, GPS_Lon, GPS_Satellite, GPS_Time

    (IP, Broadcast) = MaoGetIpBroad()

    # ser = serial.Serial("/dev/ttyAMA0", 9600)

    count = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(('0.0.0.0', 0))


    # DNSLastTime = ""
    # DNSTimeCount = 61


    while(True):
        count = count + 1

        # CPU_Temp = str(get_cpu_temp())
        # GPU_Temp = str(get_gpu_temp())
        Count = str(count)
        SysTime = str(datetime.datetime.now()).split(".")[0]
        # Env_Temp = getEnvironmentTemp("/sys/bus/w1/devices/28-00141093caff/w1_slave")
        NodeName = socket.gethostname()
        # GPS_Lat = latitude
        # GPS_Lon = longitude
        # GPS_Satellite = satellite
        # GPS_Time = str(dateTime)


        data = "IP=" + IP + ";"
        # data = data + "CPU_Temp=" + CPU_Temp + ";"
        # data = data + "GPU_Temp=" + GPU_Temp + ";"
        data = data + "Count=" + Count + ";"
        data = data + "SysTime=" + SysTime + ";" # exclude microSeconds
        # data = data + "GPS=" + latitude + "," + longitude + "," + satellite + ";"
        # data = data + "GpsTime=" + GPS_Time + ";"
        # data = data + "Temperature=" + Env_Temp + ";"
        # data = data + "DNSTime=" + DNSLastTime + ";"
        data = data + "NodeName=" + NodeName + ";"

        
        try:
            if ("1.0.8.0" == Broadcast):
                (IP, Broadcast) = MaoGetIpBroad()
                # print "Send_get " + IP + "," + Broadcast
            else:
                sock.sendto(data, (Broadcast, 7181))

                BroadcastToMasterLAN(MasterBroadcastLAN = "10.103.89.",
                                    FROM = 1,
                                    TO = 255,
                                    sock = sock,
                                    msg = data)

                # soundIP(IP)

                # if (DNSTimeCount > 60): # update per 120 seconds
                #     # urllib.urlretrieve("http://maojianweipi:6m6a5o47121@ddns.oray.com/ph/update?hostname=maojianwei.oicp.net&myip=" + IP,"/home/pi/DNSInternalResult.txt")
                #     # urllib.urlretrieve("http://maojianweipi:6m6a5o47121@ddns.oray.com/ph/update?hostname=maopi.picp.net&myip=" + IP,"/home/pi/DNSInternalResult.txt")
                #     # urllib.urlretrieve("http://maojianwei:6m6a5o47121@ddns.oray.com/ph/update?hostname=maojianwei.wicp.net","/home/pi/DNSInternetResult.txt")
                #     # DNSLastTime = str(datetime.datetime.now())
                #     DNSLastTime = "unable"
                #     DNSTimeCount = 0
                #     # print DNSLastTime
                # else:
                #     DNSTimeCount = DNSTimeCount + 1


        except:
            (IP, Broadcast) = MaoGetIpBroad()

        data = data.replace(";","</br>")
        record = open("/monitor.html", "w", 0)
        record.write("<html><head><title>BigMao Radio Station Monitor</title></head><body>")
        record.write(data)
        record.write("</body></html>")
        record.close()


        # time.sleep(1) # change from 2 to 1, for sound delay
        time.sleep(3) # for no sound


if __name__ == '__main__':
    if( len(sys.argv) > 1 ):
        My_Number = sys.argv[1]
    else:
        My_Number = "not defined"

    main()