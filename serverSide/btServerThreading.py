import bluetooth
import time
from threading import Thread
import json
from pathlib import Path

# Library of command
def listOfCommand(command):
	return{
		"ACK4S":0,
		"ACK4C":1,
		"FORWARD":2,
		"BACK":3,
		"LEFT":4,
		"RIGHT":5,
		"STOP":6,
        "UPDATE":7,
		"QUIT":98,
        "WAIT":99
	}.get(command, 100) # default will be ERROR

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
        print("Server is up!")

    def listen(self):
        backlog = 3
        print("Waiting for connection ... ")
        self.btConnect.listen(backlog)
        while True:
            client, address = self.btConnect.accept()
            #client.settimeout(60)
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
            counter = 0
            runningState = False
            data = "WAIT"

            id = -1
            compareid = -1

            queue = []

            # Second ACK the connection from client
            if listOfCommand(serverDataRecv) == 1:
                print("Connection established for "+clientName)
                # After establish connection, now start command client
                # First check if the control file is existed yet
                check = Path(fileControl);
                while(check.is_file() == False):
                # Wait until the command file is existed:
                    check = Path(fileControl);
                
                # Now we have the control file
                print("Detected commands for " +clientName)
                while True:
                    # Get command
                    if len(queue)==0 and control==0:
                        id = int(json.load(open(fileControl))["ID"])
                        if(compareid != id): # this mean we have new file
                            control = 1
                            counter = 0
                            queue = str(json.load(open(fileControl))["commands"]).split(',')
                            compareid = id
                            start = time.time()
                            data = queue[0];

                    elif len(queue) > 0 and control ==1:
                        counter = counter + 1
                        if counter == len(queue): # Stop when the queue is cleared
                            control = 0
                            queue=[]
                            data="WAIT"
                        else:
                            data = queue[counter]
                        
                    #else: #Program in wait state
                    else:
                        data = "WAIT"

                    if listOfCommand(data) != 99 :
                    # If data is valid then start sending                        
                        #Also timing the connection time
                        client.send(data)
                        # Waiting for update on position
                        serverDataRecv = client.recv(dataSize).decode("utf-8")
                        if listOfCommand(data) == 7:
                                end = time.time()
                                print("Time needed for communicate = " + str(end-start))
                                print(serverDataRecv)
                                with open(fileStatus, 'w') as outfile:
                                    outfile.write(serverDataRecv)
                            # Quit when user type quit in command line
                        elif listOfCommand(data) == 98:
                                break
                        else:
                            print("Client " + clientName+ " acknowledged the signal")

                client.close()
        return False

if __name__ == "__main__":
    # Multithreaded Python server: Bluetooth server
    hostMACAddress = '00:1A:7D:DA:71:13' # Huy Bluetooth
    #hostMACAddress = '60:6C:66:B5:63:D1' # Aleksa Bluetooth
    btPort = 3  # default for pyBluez bluetooth

    newthread = ThreadedServer(hostMACAddress, btPort)
    newthread.listen()

        #newthread.start()
        #threads.append(newthread)

        #for t in threads:
            #t.join()
