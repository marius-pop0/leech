import sys, socketserver, socket

PORT = 0
key = ""





class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFFER_SIZE = 4096

    def handle(self):

        #authorized = True  # authorization flag


        data = self.request.recv(self.BUFFER_SIZE)
        if len(data) == self.BUFFER_SIZE:
            while 1:
                try:  # error means no more data
                    data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
                except:
                    break



        #if not authorized:
            # authorized = (command[0] == password)
            #if not authorized:
             #   print(data)
                ##disconnect if password is not known
                #self.request.sendall(bytearray(incorrectPw, "UTF-8"))
              #  sys.exit(1)
            #else:
                #self.request.sendall(bytearray(welcome, "UTF-8"))



        command = data.decode("utf-8")

        if (command=="write"):
            print("Writing")




        elif(command=="read"):
            print("reading")





        else:
            print("Invalid Command Type Received")







if __name__ == '__main__':
    if len(sys.argv) == 2:
        PORT = int(sys.argv[1])
    elif len(sys.argv) == 3:
        PORT = int(sys.argv[1])
        key = sys.argv[2]

    else:
        print("wrong number of arguments")
        sys.exit(0)

    server = socketserver.ThreadingTCPServer(("localhost", PORT), MyTCPHandler)
    server.serve_forever()