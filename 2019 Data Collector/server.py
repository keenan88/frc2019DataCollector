import socket, threading
import os, csv

#SERVER STUFF
def openConnections(IP, port):
    s = socket.socket()
    s.bind((IP, port))

    s.listen(6)

    print("server started. IP- > " + IP + ", Port -> "+str(port))
    while True:
        c, addr = s.accept() #gets connection socket and ip addr
        print("Client connected: ", str(addr))
        t = threading.Thread(target=sendFile, args=("retrThread", c))
        t.start()


def sendFile(name, sock):
    headers = ['teamNum', 'matchNum', 'startingPos', 'climbLevel', 'bayCargo', 'bayHatch', 'rocketCargoLow', 'rocketCargoMid', 'rocketCargoHigh', 'rocketHatchLow', 'rocketHatchMid', 'rocketHatchHigh', 'comments']
    try:
        filename = str(sock.recv(1024), 'utf-8')

        if os.path.isfile(filename): #if requested file exists
            with open(filename, 'rb') as f: #open the file
                bytesToSend = f.read(4096) #set up the bytes to send
            f.close()
        else:
            with open(filename, 'a', newline='\n') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(headers)
            f.close()
            with open(filename, 'rb') as n: #open the file
                bytesToSend = n.read(4096) #set up the bytes to send
            n.close()


        sock.send(bytesToSend) #send bytes to client
        data = sock.recv(4096) #getting back same data, plus new client data
        with open(filename, 'wb') as n:
            n.write(data)
        n.close()

        sock.close()

    except:
        sock.send(str.encode("From Server: Ran into an error. Exception raised"))


if __name__ == '__main__':
    openConnections(socket.gethostbyname(socket.gethostname()), 5000)








