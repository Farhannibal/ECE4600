import queue


fileRead = open('../bluetoothComm/CommandQueue.txt', "r")

cmd_queue = queue.Queue()
for command in fileRead.read().split():
    cmd_queue.put(command)

while cmd_queue.empty() == False:
    value = cmd_queue.get()
    print(value)
    if value == "END":
        break
fileRead.close()

print("End of program")



# for command in fileRead.read().split():
#     if command == "UP":
#         print("Go up")
#     elif command == "DOWN":
#         print("Go down")
#     elif command == "LEFT":
#         print("Go left")
#     elif command == "RIGHT":
#         print("Go right")
#     elif command == "STOP":
#         print ("Stop the car!")
#     elif command == "END":
#         break
# print("End of program")
