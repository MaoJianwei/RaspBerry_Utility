import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 9600)

while True:
	count = ser.inWaiting()
	if count != 0:
		recv = ser.read(count)
		print recv
	#time.sleep(1)