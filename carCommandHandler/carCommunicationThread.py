import bluetooth
import threading

BUFFSIZE = 1024


# Library of command
def listOfCommand(command):
    return {
        "ACK4S": 0,
        "ACK4C": 1,
        "UP": 2,
        "DOWN": 3,
        "LEFT": 4,
        "RIGHT": 5,
        "STOP": 6,
        "QUIT": 98
    }.get(command, 99)  # default will be WAIT


class communication_thread(threading.Thread):
    def __init__(self, serverAddress):
        threading.Thread.__init__(self)
        self.serverAddress = serverAddress
        self.port = 3
        self.serverConnection = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connectToServer(self):
        # Establish connection between server and client
        self.serverConnection.connect((self.serverAddress, self.port))
        self.clientRecvData = self.serverConnection.recv(BUFFSIZE).decode("utf-8")
        self.communicate()

    def communicate(self):
        if listOfCommand(self.clientRecvData) == 0:
            self.serverConnection.send("ACK4C")
            print("Connection established")

            while True:
                # Keep listening to Server
                self.clientRecvData = self.serverConnection.recv(BUFFSIZE).decode("utf-8")

                # Error detection:
                if listOfCommand(self.clientRecvData) == 99:
                    print("Received error message, need send back new command!")
                # Else there is no error:
                else:

                    # Quit when server decide to quit
                    if self.clientRecvData == "QUIT":
                        # with open("CommandQueue.txt", "a") as output_file:
                        #     output_file.write("END" + '\n')
                        break

                    # Else follow the command
                    elif listOfCommand(self.clientRecvData) == 2:
                        print("Go up")
                    elif listOfCommand(self.clientRecvData) == 3:
                        print("Go back")
                    elif listOfCommand(self.clientRecvData) == 4:
                        print("Turn left")
                    elif listOfCommand(self.clientRecvData) == 5:
                        print("Turn right")
                    elif listOfCommand(self.clientRecvData) == 6:
                        print("Stop the car!")
                    #                 Send ACK back
                    self.serverConnection.send("ACK4C")

        print("Cut connection")
        self.serverConnection.close()

    def run(self):
        print("Start the communication with server")
        # while self.running:
        self.connectToServer()
