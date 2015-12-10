
import socket
# import struct
import time

from MaoRemoteControl import MaoRemoteControlPeer



def MaoDataTokenEncrypt(token, comCount):

	return hashlib.sha256(token + chr(comCount)).digest()


def MaoHandshakeTokenDeEncrypt(token_src):
	dst = ""

	count = 1

	high = 0
	low = 0
	charTemp = 0

	for s in token_src:

		high = 0
		low = 0
		charTemp = ord(s)

		if(1 == count):				# 10000001
			high = charTemp & 0x80
			low = charTemp & 0x01

			if (0 == high):
				charTemp = charTemp & 0xfe # low set 0
			else:
				charTemp = charTemp | 0x01 # low set 1

			if (0 == low):
				charTemp = charTemp & 0x7f # high set 0
			else:
				charTemp = charTemp | 0x80 # high set 1

			dst = dst + chr(charTemp)

			count += 1

		elif(2 == count):			# 01000010
			high = charTemp & 0x40
			low = charTemp & 0x02

			if (0 == high):
				charTemp = charTemp & 0xfd # low set 0
			else:
				charTemp = charTemp | 0x02 # low set 1

			if (0 == low):
				charTemp = charTemp & 0xbf # high set 0
			else:
				charTemp = charTemp | 0x40 # high set 1
			
			dst = dst + chr(charTemp)

			count += 1

		elif(3 == count):			# 00100100
			high = charTemp & 0x20
			low = charTemp & 0x04

			if (0 == high):
				charTemp = charTemp & 0xfb # low set 0
			else:
				charTemp = charTemp | 0x04 # low set 1

			if (0 == low):
				charTemp = charTemp & 0xdf # high set 0
			else:
				charTemp = charTemp | 0x20 # high set 1

			dst = dst + chr(charTemp)

			count += 1

		elif(4 == count):			# 00011000
			high = charTemp & 0x10
			low = charTemp & 0x08

			if (0 == high):
				charTemp = charTemp & 0xf7 # low set 0
			else:
				charTemp = charTemp | 0x08 # low set 1

			if (0 == low):
				charTemp = charTemp & 0xef # high set 0
			else:
				charTemp = charTemp | 0x10 # high set 1
			
			dst = dst + chr(charTemp)

			count = 1
		else:		# should not enter here
			pass	

	return dst


def main():
	random.random()
	random.random()
	random.random()

	conListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	print "socket"
	print conListen.bind(("0.0.0.0",1080))
	print "bind"
	print conListen.listen(0)
	print "listen"
	(remote, remoteAddr) = conListen.accept()
	print "accept"

	peer = MaoRemoteControlPeer(remoteSock = remote, remoteAddr = remoteAddr)

	peer.work()




if __name__ == '__main__':
	main()