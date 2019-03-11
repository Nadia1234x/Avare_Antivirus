import socket
import sys
from threading import Thread
import testing_server_file

#TCP connection
host = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5555

try:
    s.bind((host, port))
except socket.error as e:
    print (str(e))

s.listen(5)
print('Waiting for a connection')

def threaded_client(conn):
    conn.send(str.encode('Hello, there just practicing\n'))
    while True:
        data = conn.recv(2048)
        print data
        reply = 'Server Output:' + testing_server_file.print_something()
        if not data:
            break
        conn.sendall(reply)

        if(data == 'check credentials'):
            print 'doing'
    conn.close()



while True:

    conn, addr = s.accept()
    print 'connected to: ' + addr[0] + ':' + str(addr[1])
    #Creating a thread for the connected client.
    thread = Thread(target = threaded_client, args = (conn, ))
    thread.start()
