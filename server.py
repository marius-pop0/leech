import sys, socketserver, socket, pickle, cryptoUtils, random, string

PORT = 0
key = ""
IV=None   
					



class MyTCPHandler(socketserver.BaseRequestHandler):
	BUFFER_SIZE = 4096
	FILE_BUFSIZE = 4194304

	def handle(self):
		hostname = self.request.getsockname()
		peername = self.request.getpeername()
		print("new connection from " + hostname[0] + " from port " + str(peername[1]))

		#receiver cipher type and IV here
		
		#get the command

		data = self.request.recv(self.BUFFER_SIZE)

		l = pickle.loads(data)
		type = l[0]
		IV=b''
		if(len(l)==2):
			IV=l[1]

		#AES256
		blockSize = -1
		if(type=="aes256"):
			print("client using AES256: " +key)
			blockSize = 32
			crypto = cryptoUtils.AESCipher(key, blockSize)
		#AES128
		elif(type=="aes128"):
			print("client using AES128")
			blockSize = 16
			crypto = cryptoUtils.AESCipher(key, blockSize)
		#None
		else:
			print("client using None")
			blockSize = 0
			crypto = cryptoUtils.AESCipher(key, blockSize)

		#get command type (read/write)
		if blockSize != 0:
			data = self.request.recv(blockSize)
		else:
			data = self.request.recv(5)

		try:
			command = crypto.decrypt(data,IV)
		except:
			print("Incorrect client key")
		command = command.decode("ascii").strip('.')
		print("command: " + command) #log
		
		#get size of filename
		if blockSize != 0:
			raw_size = self.request.recv(blockSize)
		else:
			raw_size = self.request.recv(4)
		raw_size = crypto.decrypt(raw_size, IV)
		size = int.from_bytes(raw_size, 'big')
		
		#get filename
		raw_name = self.request.recv(size)
		raw_name = crypto.decrypt(raw_name, IV)
		filename = raw_name.decode("ascii")
		print("filename: " + filename)

		#filename = data.decode("ascii").strip('\n')
		
		if (command == "write"):
			print("Listening")
			#receive file
			fileData = b''
			try:
				with open(filename, "wb") as f:
					while 1:
						
						#print("Started")
						#receive chunk size
						if blockSize != 0:
							raw_size = self.request.recv(blockSize)
							if not raw_size:
								break
						else:
							#print("get size")
							raw_size = self.request.recv(4)
							if not raw_size:
								break
							#print("got size")
						
						raw_size = crypto.decrypt(raw_size,IV)
						if raw_size.decode("ascii") == "0":
							#print("done")
							break
						#print("decrypted")
						size = int.from_bytes(raw_size, 'big')
						
						#print("begin receive")
						#receive chunk\
						data = b''
						while len(data) < size:
							data += self.request.recv(size - len(data))
						
						#print("received chunk")
						
						#decrypt chunk here
						data = crypto.decrypt(data,IV)
							
						#print("appending")
						f.write(data)
							
						#print("wrote chunk")
						if size < self.FILE_BUFSIZE:
							break
				print("file write success")
				
			
			except:
				print("file write failed")
				#tell client that file write failed
				self.request.sendall(crypto.encrypt("no".encode("ascii"), IV))
				return 1
				
			print("ok")
			#send acknowledgement back to client
			self.request.sendall(crypto.encrypt("ok".encode("ascii"), IV))
			
		elif (command == "read"):
			print("Sending")
			
			try:
				with open(filename, "rb") as f:
					readData = f.read()
				#send filesize to client first
				ciphertext = crypto.encrypt(readData,IV)
				size = len(ciphertext)

				self.request.sendall(crypto.encrypt(size.to_bytes(4, 'big'),IV))
				
				self.request.sendall(ciphertext)
			except:
				print ("error reading file")
				self.request.sendall(crypto.encrypt("DNE".encode("ascii"),IV))
			
			
		else:
			print("Invalid Command Type Received: " + command)
		IV = None
		crypto = None
		self.request.close()
		print("closing connection")

		
#arguents: python2.7 server.py port [key]
if __name__ == '__main__':
	if len(sys.argv) == 2:
		PORT = int(sys.argv[1])
		key = ''.join(random.SystemRandom().choice(string.ascii_uppercase+string.ascii_lowercase + string.digits) for _ in range(32))
		print("Auto generated key: " + key)
	elif len(sys.argv) == 3:
		PORT = int(sys.argv[1])
		key = sys.argv[2]

	else:
		print("Incorrect usage: server.py port [key]")
		sys.exit(0)

	server = socketserver.ThreadingTCPServer(("localhost", PORT), MyTCPHandler)
	server.serve_forever()
