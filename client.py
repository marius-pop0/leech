import sys, socket, cryptoUtils, pickle

command = ""
filename = ""
host_port = ""
cipher = ""
key = ""
host = ""
port = 0
blockSize = -1


def write():
	BUFFER_SIZE = 4194304
	#print("writing")

	encryptAndSend(crypto, "write".encode("ascii"), IV)	

	raw_name = filename.encode("ascii")
	cipher_name = crypto.encrypt(raw_name, IV)
	# send the filename size
	name_len = len(cipher_name)
	
	encryptAndSend(crypto, name_len.to_bytes(4, 'big'), IV)
	s.sendall(cipher_name)
	#print("filename sent")

	# read file from stdin, send to server in 4MB chunks
	while 1:
		if blockSize != 0:
			chunk = sys.stdin.buffer.read(BUFFER_SIZE -16)
		else:
			chunk = sys.stdin.buffer.read(BUFFER_SIZE)

		if not chunk:  # no data was read
			break
		
		cipher = crypto.encrypt(chunk, IV)
		# encrypt chunk here
		chunk_size = len(cipher)

		# send chunk size, change chunk to the encrypted block as necessary
		encryptAndSend(crypto,chunk_size.to_bytes(4, 'big'),IV)

		# send chunk
		s.sendall(cipher)


	global blockSize
	# wait for server acknowledgement for file write
	if blockSize != 0:
		response_raw = s.recv(blockSize)
	else:
		response_raw = s.recv(2)
	response = crypto.decrypt(response_raw,IV)
	response = response.decode("ascii")
	if response == "ok":
		#print("OK")
		pass
	elif response == "no":
		print("File write failed")
	else:
		print("unknown response from server")

	s.close()


def read():
	#print("reading")
	#command
	encryptAndSend(crypto, "read.".encode("ascii"), IV)

	raw_name = filename.encode("ascii")
	ciphertext = crypto.encrypt(raw_name, IV)
	# send the filename size
	name_len = len(ciphertext)

	encryptAndSend(crypto,name_len.to_bytes(4, 'big'),IV)

	encryptAndSend(crypto, raw_name, IV)

	
	global blockSize
	
	# receive filesize
	if blockSize != 0:
		raw_size = s.recv(blockSize)
	else:
		raw_size = s.recv(4)
	
	try:
		size = crypto.decrypt(raw_size,IV)
	except:
		print("Key is incorrect")
		return 1
	# receive file
	size = int.from_bytes(size, 'big')
	data = b''
	while len(data) < size:
		data += s.recv(size)
	data = crypto.decrypt(data,IV)
	
	#write data to stdout
	sys.stdout.buffer.write(data)

	if (data == "DNE".encode("ascii")):
		print("File not found")
	#else:
		#print("ok")
	s.close()


def send(message):
	s.send(pickle.dumps(message))


def encryptAndSend(crypto, message, IV):
	s.sendall(crypto.encrypt(message, IV))

#arguments python3 client.py command filename host:port ciphertype [key]
if __name__ == '__main__':
	if len(sys.argv) == 5:
		command = sys.argv[1]
		filename = sys.argv[2]
		host_port = sys.argv[3]
		cipher = sys.argv[4]
		key = "hi"

	elif len(sys.argv) == 6:
		command = sys.argv[1]
		filename = sys.argv[2]
		host_port = sys.argv[3]
		cipher = sys.argv[4]
		key = sys.argv[5]
	else:
		print("wrong number of arguments")
		sys.exit(0)

	if (command != "write" and command != "read"):
		print("Wrong Command Parameter")
		sys.exit(0)

	host = ""
	port = 0

	try:
		host_port2 = host_port.split(":")
		host = host_port2[0]
		port = int(host_port2[1])
	except ImportError:
		print("Wrong hostname:port format")
		sys.exit(0)

	if (cipher != "aes256" and cipher != "aes128" and cipher != "none"):
		print("Wrong Cipher Parameter")
		sys.exit(0)
	if (cipher == "aes256" or cipher == "aes128"):
		if(key == ""):
			print("Must specify a key when using encryption")
			sys.exit(0)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

	s.connect((host, port))

	if (cipher == "aes256"):
		global blockSize
		blockSize = 32
		crypto = cryptoUtils.AESCipher(key, blockSize)
		IV = crypto.createIV()
		message = ["aes256", IV]
		send(message)

		if (command == "write"):
			write()
		else:
			read()

	elif (cipher == "aes128"):
		global blockSize
		blockSize = 16
		crypto = cryptoUtils.AESCipher(key, blockSize)
		IV = crypto.createIV()
		message = ["aes128", IV]
		send(message)

		if (command == "write"):
			write()
		else:
			read()
	else:
		blockSize = 0
		crypto = cryptoUtils.AESCipher(key, blockSize)
		IV = crypto.createIV()
		send(["none"])

		if (command == "write"):
			write()
		else:
			read()
