import sys

command = ""
filename = ""
host_port = ""
cipher = ""
key = ""






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
