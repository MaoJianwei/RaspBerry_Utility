import time
from os import system

def main():

	while(True):

		hour = time.localtime(time.time()).tm_hour
		minute = time.localtime(time.time()).tm_min

		if(23 == hour and minute >=20):
			record = open("/autoShutdown.html", "a", 0)
			record.write(
					str(time.localtime(time.time()).tm_year) + '.' +
					str(time.localtime(time.time()).tm_mon) + '.' +
					str(time.localtime(time.time()).tm_mday) + ' ' +
					str(time.localtime(time.time()).tm_hour) + ':' +
					str(time.localtime(time.time()).tm_min) + ':' +
					str(time.localtime(time.time()).tm_sec) + ' auto shutdown -> halt\r\n'
				)
			record.close()
			system('halt')
		time.sleep(10)



if __name__ == '__main__':

	record = open("/autoShutdown.html", "a", 0)
	record.write(
		str(time.localtime(time.time()).tm_year) + '.' +
		str(time.localtime(time.time()).tm_mon) + '.' +
		str(time.localtime(time.time()).tm_mday) + ' ' +
		str(time.localtime(time.time()).tm_hour) + ':' +
		str(time.localtime(time.time()).tm_min) + ':' +
		str(time.localtime(time.time()).tm_sec) + ' auto shutdown -> start\r\n'
	)
	record.close()
	main()