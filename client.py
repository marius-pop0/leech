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

def write():
    print("writing")
    s = socket.socket()  # Create a socket object

    s.connect((host, port))


    s.send("Hi".encode('ascii'))

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

    write()
