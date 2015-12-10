
import random
import hashlib

from remoteControl import MaoDataTokenEncrypt, MaoHandshakeTokenDeEncrypt





# print "start recv"

# command_str = remote.recv(1) 
# # command = struct.unpack('B', command_str)[0]
# command = ord(command_str)
# # if(0 != (command & 0x10)):
# # elif(0 != (comand &))

# print "finish recv"
# print len(s)	# 0 means SOCK_ERROR
# print struct.unpack('B', s)[0]

# s = 0x22
# # print struct.pack('B', s)
# # print remote.send(struct.pack('B', s))
# print remote.send(chr(s))

# print "finish send"
# time.sleep(100)

# Control Socket Status
# 0 - HANDSHAKE
# 1 - CONTROL
# 2 - GOODDAY
# 3 - TCPCLOSE


class MaoRemoteControlPeer():

	def __init__(self, *args, **kwargs):

		self.workSock = kwargs["remoteSock"]
		self.status = 0

		self.token = ""
		self.tokenDeEnCount = 1


	def handshake(self):
		print "handshake"

		if(0 != self.status):
			return False

		random.random()
		random.random()
		random.random()

		self.token = hashlib.sha256(str(int(random.random()*1000))).digest()
		token_secret = MaoHandshakeTokenDeEncrypt(token_src = self.token)

		self.workSock.send(chr(0x88) + token_secret)

		self.status = 1
		return True
		
		# command = ord(self.workSock.recv(1))

		# if(0 != command & 0x80 and
		# 	0 != command & 0x01):
			
		# 	token_origin = MaoHandshakeTokenDeEncrypt(token_src = self.workSock.recv(32))
		# 	if(token_origin == self.token):

				# self.status = 1
				# return True

		# 	else:
		# 		return False

		# else:
		# 	return False

	def work(self):
		print "work"

		if(False == self.handshake()):
			print "++++++ handshake false ++++++"
			self.forceRelease()
			return

		if(1 != self.status):
			print "++++++ self.status != 1 ++++++"
			self.forceRelease()
			return

		while(True):

			# command = struct.unpack('B', command_str)[0]
			command = ord(self.workSock.recv(1))

			recvToken = self.workSock.recv(32)
			calToken = MaoDataTokenEncrypt(token = recvToken, comCount = self.tokenDeEnCount)
			if(255 == self.tokenDeEnCount):
				self.tokenDeEnCount = 1
			else:
				self.tokenDeEnCount = self.tokenDeEnCount + 1

			if(calToken != recvToken):
				print "++++++ work token_secret false ++++++"
				self.forceRelease()
				return


			
			if(0 != command & 0x40):
				if(0 == command & 0x08):
					self.forceRelease()
					return

				self.status = 2
				if(False == self.goodDay()):
					print "++++++ goodDay false ++++++"
					self.forceRelease()
					return
				else:
					return
					
			elif(0 != command & 0x20):
				
				if(0 != command & 0x08):
					CMD = command & 0x07
					if(0 == CMD):
						pass # reboot

					elif()
					pass # TODO
				else:
					cID = = command & 0x07
					pass # TODO

			else:		# should not enter here
				print "======== ERROR_Command ========"

		return 

	def goodDay(self):
		print "goodDay"
		if(2 != self.status):
			return False

		token_secret = MaoDataTokenEncrypt(token = self.token, comCount = self.tokenDeEnCount)
		if(255 == self.tokenDeEnCount):
			self.tokenDeEnCount = 1
		else:
			self.tokenDeEnCount = self.tokenDeEnCount + 1

		self.workSock.send(chr(0x41) + token_secret)

		self.status = 3
		self.forceRelease()


	def forceRelease(self):
		self.token = ""
		self.tokenDeEnCount = 1
		self.status = 3
		self.workSock.shutdown(socket.SHUT_RDWR)
		self.workSock.close()