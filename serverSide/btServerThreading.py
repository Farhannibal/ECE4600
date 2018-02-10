import bluetooth
import time
from threading import Thread
import json

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

def namesOfCars(MACAddress):
    return{
        "34:C3:D2:BF:1D:1A":"bigPine",
        "34:C3:D2:C2:86:17":"Pen",
        "34:C3:D2:C0:0E:6D":"Pineapple",
        "34:C3:D2:F8:C9:50":"Apple",
        "34:C3:D2:F8:D6:D1":"Hoodie",
        }.get(MACAddress, "nosupport")


class ThreadedServer(Thread):
    def __init__(self, hostMAC, port):
        #Thread.__init__(self)
        self.hostMAC = hostMAC
        self.port = port
        self.btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.btConnect.bind((hostMACAddress, port))
        self.numberOfConnection = 0
        print("Server is up!")

    def listen(self):
        backlog = 3
        print("Waiting for connection ... ")
        self.btConnect.listen(backlog)
        while True:
            client, address = self.btConnect.accept()
            client.settimeout(60)
            #(client, (MACconnect, port)) = btConnect.accept()
            Thread(target = self.listenToClient, args = (client, address)).start()

    # Method to establish the new connection for each thread
    def listenToClient(self, client, clientInfo):
        dataSize = 1024
         # First check if client is in our support
        clientName = namesOfCars(str(clientInfo[0]))

        # Reject if it's not in the system
        if (clientName =="nosupport"):
            client.close()
        else :
             # Check if client finish estasblishing connection
            client.send("ACK4S")
            serverDataRecv = client.recv(dataSize)
            serverDataRecv = serverDataRecv.decode("utf-8")
            fileControl = "Traffic_Sim/Assets/"+ clientName + "Control.json"
            fileStatus = "Traffic_Sim/Assets/"+ clientName + "Status.json"

            control = 0
            #control = 2

            counter = 1
            queue = []

            # Second ACK the connection from client
            if listOfCommand(serverDataRecv) == 1:
                print("Connection established for "+clientName)
                self.numberOfConnection += 1
                while True:
                    # After establish connection, now start command client
                    if control == 0:
                        queue = str(json.load(open(fileControl))["commands"]).split(',')
                        control = 1
                        data = queue[0]
                    elif len(queue) > counter:
                        data = queue[counter]
                        counter = counter + 1
                    else:
                        print("Please enter command for "+clientName+": ")
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
                        with open(fileStatus, 'w') as outfile:
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
    #hostMACAddress = '5C:F3:70:76:B6:5E' # Huy Bluetooth
    hostMACAddress = '60:6C:66:B5:63:D1' # Aleksa Bluetooth
    btPort = 3  # default for pyBluez bluetooth

     #Spawn thread
    #threads = []

    #while True:
        #btConnect.listen(1)  # this will send to back log
        
    newthread = ThreadedServer(hostMACAddress, btPort)
    newthread.listen()

        #newthread.start()
        #threads.append(newthread)

        #for t in threads:
            #t.join()
