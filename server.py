import sys, socketserver, socket, hashlib, binascii, time

PORT = 0
key = ""

class MyTCPHandler(socketserver.BaseRequestHandler):
	BUFFER_SIZE = 4096
	FILE_BUFSIZE = 4194304

	def handle(self):
		hostname = self.request.getsockname()
		peername = self.request.getpeername()
		print("new connection from " + hostname[0] + " from port " + str(peername[1]))
		#receiver cipher type and IV here
		
		#get the command
		data = self.request.recv(5)
		
		command = data.decode("ascii").strip('.')
		
		#get size of filename
		raw_size = self.request.recv(4)
		size = int.from_bytes(raw_size, 'big')
		
		#get filename
		raw_name = self.request.recv(size)
		filename = raw_name.decode("ascii")
		
		print("command: " + command) #log
		
		if (command == "write"):
			print("Writing")
			
			#receive file
			fileData = b''
			
			while 1:
				#receive chunk size
				raw_size = self.request.recv(4)
				size = int.from_bytes(raw_size, 'big')
				
				#receive chunk\
				data = self.request.recv(size)
				if not data:
					break
				#decrypt chunk here
				fileData += data
				if size < self.FILE_BUFSIZE:
					break
			try:
				with open(filename, "wb") as f:
					f.write(fileData)
				print("file write success")
			except:
				print("file write failed")
				#tell client that file write failed
				self.request.sendall("no".encode("ascii"))
				return 1
				
			print("ok")
			#send acknowledgement back to client
			self.request.sendall("ok".encode("ascii"))
			
		elif (command == "read"):
			print("reading")
			
			try:
				with open(filename, "rb") as f:
					readData = f.read()
				#send filesize to client first
				size = len(readData)
				self.request.sendall(size.to_bytes(4, 'big'))
				
				self.request.sendall(readData)
				
				logOutput = readData.decode("ascii")
				print(logOutput)
			except:
				print ("error reading file")
				self.request.sendall("DNE".endcode("ascii"))
			
			
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