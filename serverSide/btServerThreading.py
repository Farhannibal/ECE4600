import bluetooth
from commandList import listOfCommand
from threading import Thread


class ThreadedServer(Thread):
    def __init__(self, clientMAC, port):
        Thread.__init__(self)
        self.clientMAC = clientMAC
        self.port = port

    def run(self):
        dataSize = 1024
        while True:
            # First check if client finish estasblishing connection
            client.send("ACK4S")
            serverDataRecv = client.recv(dataSize)
            serverDataRecv = serverDataRecv.decode("utf-8")

            # Second ACK the connection from client
            if listOfCommand(serverDataRecv) == 1:
                print("Connection established for "+self.clientMAC+" at port: "+str(self.port))
                while 1:
                    # After establish connection, now start command client
                    data = input("Enter command for client with MAC: "+self.clientMAC+" at port: "+str(self.port))
                    if listOfCommand(data) != 99:
                        # If data is valid then start sending

                        client.send(data)

                        # Waiting for ACK signal
                        serverDataRecv = client.recv(dataSize).decode("utf-8")

                        # If ACK then keep going, if not resend data
                        if listOfCommand(serverDataRecv) != 1:
                            client.send(data)

                        # if more than this point, give up on sending that --
                        #  think more

                        # Quit when user type quit in command line
                        if data == "QUIT":
                            # client.close()
                            break
                    else:
                        print("Wrong command, please check the command list and repeat input !")
        return False


# Multithreaded Python server: Bluetooth server
hostMACAddress = '5C:F3:70:76:B6:5E'
btPort = 3  # default for pyBluez bluetooth
backlog = 1
dataSize = 1024

btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
btConnect.bind((hostMACAddress, btPort))
# Spawn thread
threads = []

while True:
    btConnect.listen(1)  # this will send to back log
    (client, (MACconnect, port)) = btConnect.accept()
    newthread = ThreadedServer(MACconnect, port)
    newthread.start()
    threads.append(newthread)

    for t in threads:
        t.join()
