import sys
import socket
PORT = 5555


try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('connecting to the server')
s.connect(('localhost', 5555))



#Receive data
reply = s.recv(4096)
print reply

file_name = "t_file/lorem_ipsum=.txt"
f = open(file_name, 'a')
f.write("X")
f.close()
f = open(file_name, 'rb')

file_content = f.read(2048)
count = 0

while file_content:
    print 'sending'
    count = count + 1
    if(count == 1):
        file_content = "file upload" + "&-&" + file_content
    else:
        file_content = f.read(2048)
    s.send(file_content)
print 'completed sending'
f.close()
