import sys, socket

command = ""
filename = ""
host_port = ""
cipher = ""
key = ""
host= ""
port = 0




def read():
	print("reading")
	#command
	s.sendall("read.".encode("ascii"))
	
	raw_name = filename.encode("ascii")
	#send the filename size
	name_len = len(raw_name)
	s.sendall(name_len.to_bytes(4, 'big'))
	
	s.sendall(raw_name)
	
	#receive filesize
	raw_size = s.recv(4)
	size = int.from_bytes(raw_size, 'big'))
	
	#receive file
	data = s.recv(size)
	if data.decode("ascii") == "DNE":
		print("file read unsuccessful")
	else:
		print("ok")
	
	s.close()

def write():
	BUFFER_SIZE = 4194304
	print("writing")
	s.sendall("write".encode('ascii'))
	
	raw_name = filename.encode("ascii")
	#send the filename size
	name_len = len(raw_name)
	s.sendall(name_len.to_bytes(4, 'big'))
	
	s.sendall(raw_name)
	
	#read file from stdin, send to server in 4MB chunks
	while 1:
		chunk = sys.stdin.buffer.read(BUFFER_SIZE)
		
		if not chunk: #no data was read
			break
		
		#encrypt chunk here
		chunk_size = len(chunk)
		
		#send chunk size, change chunk to the encrypted block as necessary
		s.sendall(chunk_size.to_bytes(4, 'big'))
		
		#send chunk
		s.sendall(chunk)
		
		#if chunk_size < BUFFER_SIZE:
		#	break
	
	
	#wait for server acknowledgement for file write
	response_raw = s.recv(2)
	response = response_raw.decode("ascii")
	if response == "ok":
		print("OK")
	elif response == "no":
		print("File write failed")
	else:
		print("unknown response from server")
	
	s.close()



if __name__ == '__main__':
	if len(sys.argv) == 5:
		command = sys.argv[1]
		filename = sys.argv[2]
		host_port = sys.argv[3]
		cipher = sys.argv[4]
	elif len(sys.argv) == 6:
		command = sys.argv[1]
		filename = sys.argv[2]
		host_port = sys.argv[3]
		cipher = sys.argv[4]
		key = sys.argv[5]
	else:
		print("wrong number of arguments")
		sys.exit(0)

	if(command!="write" and command!="read"):
		print("Wrong Command Parameter")
		sys.exit(0)

	host=""
	port=0

	try:
		host_port2 = host_port.split(":")
		host=host_port2[0]
		port=int(host_port2[1])
	except ImportError:
		print("Wrong hostname:port format")
		sys.exit(0)

	if (cipher != "aes256" and cipher != "aes128" and cipher != "none"):
		print("Wrong Cipher Parameter")
		sys.exit(0)
	
	s = socket.socket()  # Create a socket object

	s.connect((host, port))
	
	if command == "write":
		write()
	else:
		read()
