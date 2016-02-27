import re
import subprocess
import commands
import socket
import fcntl
import struct
import time
# import serial
import datetime
import urllib
import os
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

def MaoChangeIP01(ip_string):

    newString = ""

    for s in ip_string:
        if("0" == s):
            newString = newString + "1"
        else:
            newString = newString + "0"

    return newString



# def get_cpu_temp():
#     tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
#     cpu_temp = tempFile.read()
#     tempFile.close()
#     return float(cpu_temp)/1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32

# def get_gpu_temp():
#     gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
#     return  float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32
 
def MaoGetIpBroad():

    IP_mask_str = find_all_mask()
    if("1.0.8.0" == IP_mask_str):
        return ("7.1.8.1", "1.0.8.0")

    IP_mask_num = struct.unpack("!L", socket.inet_aton(find_all_mask()))[0]
    IP_mask_num = int(MaoChangeIP01(bin(IP_mask_num)[2:]),2)

    try:
        IP_num = struct.unpack("!L", socket.inet_aton(get_ip_address("eth0")))[0]

        Broadcast_num = IP_mask_num | IP_num

        Broadcast = socket.inet_ntoa(struct.pack('!L',(IP_mask_num | IP_num)))
        IP = get_ip_address("eth0")
    except:
        IP = "7.1.8.1"
        Broadcast = "1.0.8.0"

    return (IP, Broadcast)


def soundIP(doIP):
    os.system('espeak -ven+f3 -k5 -s100 "Hello, this is Big Mao Server node six"')
    IPpiece = doIP.split('.')

    for piece in IPpiece:
        os.system("espeak -ven+f3 -k5 -s100 ." + piece)

    return



def BroadcastToMasterLAN(MasterBroadcastLAN, FROM, TO, sock, msg):
    for i in range(FROM, TO):
        sock.sendto(msg, (MasterBroadcastLAN + str(i), 7181))


def main():

    (IP, Broadcast) = MaoGetIpBroad()

    # ser = serial.Serial("/dev/ttyAMA0", 9600)
    
    count = 0
    serialCount = 5

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(('0.0.0.0', 0))


    DNSLastTime = ""
    DNSTimeCount = 61

    while(True):
        temperatureData = ""
        # while(True):
        #     if(0 != ser.inWaiting()):
        #         temperatureData += ser.read(1)
        #         if(";" == temperatureData[-1]):
        #             break
        #     elif("" == temperatureData):
        #         break
        #     elif(0 == serialCount):
        #         serialCount = 5
        #         temperatureData = ""
        #         break
        #     else:
        #         serialCount = serialCount - 1
        #         time.sleep(1)



        count = count + 1
        data = "IP=" + IP + ";"
        # data = data + "CPU_Temp=" + str(get_cpu_temp()) + ";"
        # data = data + "GPU_Temp=" + str(get_gpu_temp()) + ";"
        data = data + "Count=" + str(count) + ";"
        data = data + "Time=" + str(datetime.datetime.now()) + ";"
        data = data + "Temperature=" + temperatureData + ";"
        data = data + "DNSTime=" + DNSLastTime + ";"
        data = data + "NodeName=" + socket.gethostname() + ";"

        
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
                                    msg = "Master Broadcast " + data)

                # soundIP(IP)

                if (DNSTimeCount > 60): # update per 120 seconds
                    # urllib.urlretrieve("http://maojianweipi:6m6a5o47121@ddns.oray.com/ph/update?hostname=maojianwei.oicp.net&myip=" + IP,"/home/pi/DNSInternalResult.txt")
                    # urllib.urlretrieve("http://maojianweipi:6m6a5o47121@ddns.oray.com/ph/update?hostname=maopi.picp.net&myip=" + IP,"/home/pi/DNSInternalResult.txt")
                    # urllib.urlretrieve("http://maojianwei:6m6a5o47121@ddns.oray.com/ph/update?hostname=maojianwei.wicp.net","/home/pi/DNSInternetResult.txt")
                    # DNSLastTime = str(datetime.datetime.now())
                    DNSLastTime = "unable"
                    DNSTimeCount = 0
                    # print DNSLastTime
                else:
                    DNSTimeCount = DNSTimeCount + 1

            # print DNSTimeCount

                # print "send to " + Broadcast
        except:
            # print "trans Error"
            (IP, Broadcast) = MaoGetIpBroad()
            # print "get " + IP + "," + Broadcast

        data = data.replace(";","</br>")
        record = open("/monitor.html", "w", 0)
        record.write("<html><head><title>BigMao Radio Station Monitor</title></head><body>")
        record.write(data)
        record.write("</body></html>")
        record.close()

        time.sleep(15) # change from 2 to 1, for sound delay
 
if __name__ == '__main__':
    main()