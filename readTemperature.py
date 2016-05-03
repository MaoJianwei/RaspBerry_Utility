




temperature = ""
try:
    tempFile = open("/sys/bus/w1/devices/28-00141093caff/w1_slave")
    tempText = tempFile.read()
    tempFile.close()

    tempText = tempText.split("\n")
    if(len(tempText) == 3):
        tempText = tempText[1].split("=")
        if(len(tempText) == 2):
            temperature = str(float(tempText[1])/1000)
except:
    temperature = "unable"

print temperature
