# Updated version

import bluetooth
import threading

BUFFSIZE = 1024


# Library of command
def listOfCommand(command):
    return {
        "ACK4S": 0,
        "ACK4C": 1,
        "FORWARD": 2,
        "BACK": 3,
        "LEFT": 4,
        "RIGHT": 5,
        "STOP": 6,
        "UPDATE": 7,
        "START": 8,
        "LEFTBACK": 9,
        "RIGHTBACK": 10,
        "QUIT": 98
    }.get(command, 99)  # default will be WAIT


def messageHandler(connection, message, robot):
    # return:   True to keep the loop
    #           False to exit the loop
    # Error detection:
    if listOfCommand(message) == 99:
        print("Received error message, need send back new command!")
        return True
    # Else there is no error:
    else:
        # Quit when server decide to quit
        if message == "QUIT":
            return False
        else:
            # Else follow the command
            # Any command for the car will be modified here

            # Going forward
            if listOfCommand(message) == 2:
                print("Go forward")
                robot.command('fwd1')
                dataSendBack = "ACK4C"

            # Going back
            elif listOfCommand(message) == 3:
                print("Go back")
                robot.command('bck1')
                dataSendBack = "ACK4C"
            
            # Turn left
            elif listOfCommand(message) == 4:
                print("Turn left")
                robot.command('fwdLTurn')
                dataSendBack = "ACK4C"

            # Turn right
            elif listOfCommand(message) == 5:
                print("Turn right")
                robot.command('fwdRTurn')
                dataSendBack = "ACK4C"

            # STOP
            elif listOfCommand(message) == 6:
                print("Stop the car!")
                robot.command('stop')
                dataSendBack = "ACK4C"

            # UPDATE
            elif listOfCommand(message) == 7:
                dataSendBack = robot.status()

            # START
            elif listOfCommand(message) == 8:
                print("Start the car!")
                robot.command('start')
                dataSendBack = "ACK4C"

            # Turn left backwards
            elif listOfCommand(message) == 9:
                print("Turn left")
                robot.command('bckLTurn')
                dataSendBack = "ACK4C"

            # Turn right backwards
            elif listOfCommand(message) == 10:
                print("Turn right")
                robot.command('bckRTurn')
                dataSendBack = "ACK4C"

            # Send back when the car finish they go:
            
            connection.send(dataSendBack)
            return True


class communication_thread(threading.Thread):
    def __init__(self, serverAddress,robot):
        threading.Thread.__init__(self)
        self.serverAddress = serverAddress
        self.robot=robot ## Adds the robot to queue up comands
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

            listening = True
            while listening:
                # Keep listening to Server
                self.clientRecvData = self.serverConnection.recv(BUFFSIZE).decode("utf-8")
                listening = messageHandler(self.serverConnection, self.clientRecvData, self.robot)

        print("Cut connection")
        self.robot.command('terminate')
        self.serverConnection.close()

    def run(self):
        print("Start the communication with server")
        # while self.running:
        self.connectToServer()
