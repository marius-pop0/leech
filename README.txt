Created by 	Herman Kwan ID: 10136644
			Marius Pop ID: 10102480

Compile

	Run Server:
		python3 server.py port [key]

		ex.
		python3 server.py 9999 myKey
		

	Run Client:
		python3 read/write filename hostname:port none/aes128/aes256 [key]

		ex.
		python3 read f1.txt localhost:9999 aes256 myKey
		python3 write f1.txt localhost:9999 aes256


Protocol Description

	1. Server waits for client to connect
	2. On connect the client sends through plaintext an array including [encryption_type,IV]
	3. The client will then encrypt and send the command (read or write)
	4. The client encrypts and sends the size of filename
	5. The client encrypts and sends the filename

	On Write:

	6. The client encrypts sends the size of each chuck being sent - We set the chunk size to 4Mb
	7. The client encrypts and sends the chunk
	**Repeat step 6 and 7 untill the entire file is transfered
	8. The server will encrypt and send "ok" on success

	On Read:

	6. Server opens the file from disk, encrypts it.
	7. Server encrypts and sends the size of the encrypted file to the client
	8. Server sends the encrypted file to the client

Testing with Checksum

	dd if=/dev/urandom bs=1K iflag=fullblock count=50K > 50MB.bin

	sha256sum 50MB.bin
	e49732cfb276f3673d2cc9c9044329fbc16c0ed03cec7ff293c2b0d2b91046eb  50MB.bin

	python3 client.py write test localhost:9999 aes256 secret123 < 50MB.bin

	python3 client.py read test localhost:9999 aes256 secret123 | sha256sum
	e49732cfb276f3673d2cc9c9044329fbc16c0ed03cec7ff293c2b0d2b91046eb

Timing

