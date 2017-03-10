import sys, socketserver, socket, hashlib, binascii, time

PORT = 0
key = ""

def receiveData(self, socket):
	BUFFER_SIZE = 4096
	incoming = self.request.recv(BUFFER_SIZE)
	if len(incoming) == BUFFER_SIZE:
		while 1:
			try:  # error means no more data
				incoming += self.request.recv(BUFFER_SIZE, socket.MSG_DONTWAIT)
			except:
				break
		return incoming		   
					



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
		if len(data) == self.BUFFER_SIZE:
			while 1:
				try:  # error means no more data
					data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
				except:
					break
		
		command = data.decode("ascii").strip('\n')
		
		#both read and write need filename, so do it here
		data = self.request.recv(self.BUFFER_SIZE)
		if len(data) == self.BUFFER_SIZE:
			while 1:
				try:  # error means no more data
					data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
				except:
					break
		filename = data.decode("ascii").strip('\n')
		print("command: " + command) #log
		
		if (command == "write"):
			print("Writing")
			
			#receive file
			fileData = b''
			
			while 1:
				sleep(0.35)
				data = self.request.recv(self.FILE_BUFSIZE)
				if data:
					fileData += data
					if len(data) < self.FILE_BUFSIZE:
						break
				else:
					break
			#encrypt fileData here
			try:
				with open(filename, "wb") as f:
					f.write(fileData)
				print("file write success")
			except:
				print("file write failed")
				return 1
				
			print("ok")
			#send acknowledgement back to client
			self.request.sendall("ok".encode("ascii"))
			
		elif (command == "read"):
			print("reading")
			#read data from file
			
			try:
				with open(filename, "rb") as f:
					readData = f.read()
				logOutput = readData.decode("ascii")
				print(logOutput)
			except:
				print ("error reading file")
				self.request.sendall(b"DNE")

			
			#calculate SHA-1 hash for file
			m = hashlib.sha224()
			m.update(readData)
			hash = m.digest()
			
			print(binascii.hexlify(hash))
			
			#send file and hash back to client
			self.request.sendall(readData)
			self.request.sendall(hash)
			
		else:
			print("Invalid Command Type Received: " + command)
		self.request.close()
		print("closing connection")
		

		
#arguents: python3 server.py port [key]
if __name__ == '__main__':
	if len(sys.argv) == 2:
		PORT = int(sys.argv[1])
	elif len(sys.argv) == 3:
		PORT = int(sys.argv[1])
		key = sys.argv[2]

	else:
		print("Incorrect usage: server.py port [key]")
		sys.exit(0)

	server = socketserver.ThreadingTCPServer(("localhost", PORT), MyTCPHandler)
	server.serve_forever()