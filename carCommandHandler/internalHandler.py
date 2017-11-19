fileRead = open('../bluetoothComm/CommandQueue.txt', "r")
for command in fileRead.read().split():
    if command == "UP":
        print("Go up")
    elif command == "DOWN":
        print("Go down")
    elif command == "LEFT":
        print("Go left")
    elif command == "RIGHT":
        print("Go right")
    elif command == "STOP":
        print ("Stop the car!")
    elif command == "END":
        break
print("End of program")
