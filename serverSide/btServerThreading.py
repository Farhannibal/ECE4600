import bluetooth
from threading import Thread
import time

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
        self.btConnect.bind((hostMACAddress, port))
        self.numberOfConnection = 0
        print("Server is up!")

    # Server will keep listening for new thread
    def listenerActivate(self):
        backlog = 3
        print("Waiting for connection ... ")
        self.btConnect.listen(backlog)
        while True:
            client, address = self.btConnect.accept()
            client.settimeout(60)
            Thread(target = self.listenToClient, args = (client, address)).start()

    # Method to establish the new connection for each thread
    def listenToClient(self, client, clientInfo):
        dataSize = 1024
         # First check if client finish estasblishing connection
        client.send("ACK4S")
        serverDataRecv = client.recv(dataSize)
        serverDataRecv = serverDataRecv.decode("utf-8")

        #control = 0
        control = 2

        counter = 1
        queue = []

        # Second ACK the connection from client
        if listOfCommand(serverDataRecv) == 1:
            print("Connection established for "+str(clientInfo))
            self.numberOfConnection += 1
            while True:
                # After establish connection, now start command client
                if control == 0:
                    queue = str(json.load(open("Traffic_Sim/Assets/CarData.json"))["commands"]).split(',')
                    control = 1
                    data = queue[0]
                elif len(queue) > counter:
                    data = queue[counter]
                    counter = counter + 1
                else:
                    print("Please enter command for "+str(clientInfo)+": ")
                    print("Available commands are UP, DOWN, LEFT, RIGHT, STOP or QUIT: ")
                    data = input()

                if listOfCommand(data) != 99:
                # If data is valid then start sending

                #Also timing the connection time
                    start = time.time()
                    client.send(data)
                    
                    # Waiting for update on position
                    serverDataRecv = client.recv(dataSize).decode("utf-8")
                    end = time.time()

                    print("Time needed for update = " + str(end-start))

                    print(serverDataRecv)
                    #with open('Traffic_Sim/Assets/data.json', 'w') as outfile:
                    with open('data.json', 'w') as outfile:
                        outfile.write(serverDataRecv)
                    # Quit when user type quit in command line
                    if data == "QUIT":
                        break
                else:
                    print("Wrong command, please check the command list and repeat input !")
            client.close()
        return False

if __name__ == "__main__":
    # Multithreaded Python server: Bluetooth server
    hostMACAddress = '5C:F3:70:76:B6:5E'
    btPort = 3  # default for pyBluez bluetooth

    newthread = ThreadedServer(hostMACAddress, btPort)
    newthread.listenerActivate()

        

    #This program keep listening for new thread

