import sys

port = 0
key = ""




if __name__ == '__main__':
    if len(sys.argv) == 2:
        command = int(sys.argv[1])
    elif len(sys.argv) == 3:
        command = int(sys.argv[1])
        key = sys.argv[2]

    else:
        print("wrong number of arguments")
        sys.exit(0)
