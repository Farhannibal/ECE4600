import bluetooth
from threading import Thread

# Library of command
def listOfCommand(command):
	return{
		"ACK4S":0,
		"ACK4C":1,
		"UP":2,
		"DOWN":3,
		"LEFT":4,
		"RIGHT":5,
		"STOP":6,
		"QUIT":98
	}.get(command, 99) # default will be WAIT

class ThreadedServer(Thread):
    def __init__(self, hostMAC, port):
        #Thread.__init__(self)
        self.hostMAC = hostMAC
        self.port = port
        self.btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.btConnect.bind((hostMACAddress, btPort))
        print("Server is up!")

    def listen(self):
        backlog = 3
        print("Waiting for connection ... ")
        self.btConnect.listen(backlog)
        while True:
            client, address = self.btConnect.accept()
            client.settimeout(60)
            Thread(target = self.listenToClient, args = (client, address)).start()

    def listenToClient(self, client, address):
       
        dataSize = 1024
        # First check if client finish estasblishing connection
        client.send("ACK4S")
        serverDataRecv = client.recv(dataSize)
        serverDataRecv = serverDataRecv.decode("utf-8")

        # Second ACK the connection from client
        if listOfCommand(serverDataRecv) == 1:
            print("Connection established for "+str(address))
            while True:
                # After establish connection, now start command client
                data = input("Enter command for client: "+str(address))
                if listOfCommand(data) != 99:
                    # If data is valid then start sending
                    client.send(data)
                    
                    # Waiting for update on position
                    serverDataRecv = client.recv(dataSize).decode("utf-8")
                    print(serverDataRecv)
                    #with open('Traffic_Sim/Assets/data.json', 'w') as outfile:
                    #with open('data.json', 'w') as outfile:
                        #outfile.write(serverDataRecv)
                    # Quit when user type quit in command line
                    if data == "QUIT":
                        break
                else:
                    print("Wrong command, please check the command list and repeat input !")
        return False

if __name__ == "__main__":
    # Multithreaded Python server: Bluetooth server
    hostMACAddress = '5C:F3:70:76:B6:5E'
    btPort = 3  # default for pyBluez bluetooth

     #Spawn thread
    #threads = []

    #while True:
        #btConnect.listen(1)  # this will send to back log
        #(client, (MACconnect, port)) = btConnect.accept()
    newthread = ThreadedServer(hostMACAddress, btPort)
    newthread.listen()

        #newthread.start()
        #threads.append(newthread)

        #for t in threads:
            #t.join()
