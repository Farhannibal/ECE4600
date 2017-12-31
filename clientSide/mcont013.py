import RPi.GPIO as GPIO

import asyncio
from random import randint
import queue
import time
import json

import carCommunicationThread as communication

class Motor:
    def __init__(self, en_pin, in_pin, out_pin):
        self.en_pin = en_pin
        self.in_pin = in_pin
        self.out_pin = out_pin

        self.pwm = None
        self.dc = 0

    def setup(self, freq, dc):
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.setup(self.in_pin, GPIO.OUT)
        GPIO.setup(self.out_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.en_pin, freq)
        self.dc = dc
        self.pwm.start(self.dc)

    def cw(self):
        print('cw')
        GPIO.output(self.in_pin, True)
        GPIO.output(self.out_pin, False)

    def ccw(self):
        print('ccw')
        GPIO.output(self.in_pin, False)
        GPIO.output(self.out_pin, True)

    def stop(self):
        GPIO.output(self.in_pin, False)
        GPIO.output(self.out_pin, False)

    def changeSpeed(self, mSpeed):
        self.dc = mSpeed
        self.pwm.ChangeDutyCycle(self.dc)

    # ToDo: Add IR Sensor to adjust speed
    #
    #
    #

    def cleanup(self):
        self.pwm.stop()


class IR:
    def __init__(self, pin, motor):
        self.pin = pin
        self.motor = motor

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def check(self):
        # Checks GPIO.input(self.pin) and performs the appropriate operation
        detect = False
        if GPIO.input(self.pin):
            #print(self.__class__.__name__ + ': Input was HIGH')
            if self.motor.dc != speed:
                self.motor.changeSpeed(speed)
            detect = False
        else:
            #print("%i" + ': Input was TRUE',self.pin)
            if self.motor.dc != speed - 5:
                self.motor.changeSpeed(speed - speedDelta)
                #self.motor.changeSpeed(speed - 5)
            detect = True
        return detect


class MotorCoordinator:
    FREQ = 500

    EN1 = 26
    I1 = 2
    O1 = 3
    DC1 = 95

    EN2 = 13
    I2 = 17
    O2 = 27
    DC2 = 95

    speed = 95

    scanNode = False
    inProg = False

    def __init__(self, evt_loop):
        self.evt_loop = evt_loop
        self.motor1 = Motor(self.EN1, self.I1, self.O1)
        self.motor2 = Motor(self.EN2, self.I2, self.O2)
        self.IRL = IR(21, self.motor1)
        self.IRR = IR(16, self.motor2)

        self.motor1.setup(self.FREQ, self.DC1)
        self.motor2.setup(self.FREQ, self.DC2)
        self.IRL.setup()
        self.IRR.setup()

    def cw_motor(self, motor, start, end):
        # print('cw_motor')
        self.schedule(motor.cw, start)
        self.schedule(motor.stop, end)
        # self.schedule(self.taskComplete(), end)

    def ccw_motor(self, motor, start, end):
        self.schedule(motor.ccw, start)
        self.schedule(motor.stop, end)

    def cw_motorForever(self, motor):
        print('cw_motorForever')
        motor.cw
        self.schedule(motor.cw, 0)
        # Create Future?

    def ccw_motorForever(self, motor):
        motor.ccw
        self.schedule(motor.ccw, 0)

    def scheTaskComplete(self, end):
        # print('schedule')
        self.schedule(self.taskComplete, end)

    def taskComplete(self):
        # print('schedule')
        self.inProg = False

    def schedule(self, func, delay):
        # print('schedule')
        self.evt_loop.call_later(delay, func)

    def pollSensors(self):
        ## Scan for the Node before???
        if (self.scanNode and self.IRL.check() and self.IRR.check()):
            print('reached node')
            self.motor1.stop()
            self.motor2.stop()
            self.scanNode = False
            self.inProg = False

    def pollSensorsExitNode(self):
        ## Scan for the Node before???
        if (self.IRL.check() or self.IRR.check()):
            print('reached node')
            #self.motor1.stop()
            #self.motor2.stop()
            #self.scanNode = False
            #self.inProg = False

    def setScanNode(self, scan):
        self.scanNode = scan

    def setInProg(self):
        self.inProg = True

    def cleanup(self):
        self.motor1.cleanup()
        self.motor2.cleanup()
        GPIO.cleanup()


class MotionCoordinator:
    def __init__(self, motor_coordinator):
        self.mc = motor_coordinator
        self.inProg = False

    def forward(self, start, end):
        # print('forward')
        self.mc.setInProg()
        self.mc.cw_motor(self.mc.motor1, start, end)
        self.mc.cw_motor(self.mc.motor2, start, end)
        self.mc.scheTaskComplete(end)

    def backward(self, start, end):
        self.mc.ccw_motor(self.mc.motor1, start, end)
        self.mc.ccw_motor(self.mc.motor2, start, end)

    def forwardUntil(self):
        # print('forward')
        self.mc.setInProg()
        self.mc.cw_motorForever(self.mc.motor1)
        self.mc.cw_motorForever(self.mc.motor2)
        self.mc.setScanNode(True)

    def backwardUntil(self):
        self.mc.setInProg()
        self.mc.ccw_motorForever(self.mc.motor1)
        self.mc.ccw_motorForever(self.mc.motor2)
        self.mc.setScanNode(True)

    def turnRightFwIndef(self):
        self.mc.setInProg()
        self.mc.ccw_motorForever(self.mc.motor1)
        self.mc.cw_motorForever(self.mc.motor2)
        self.mc.setScanNode(True)

    def turnRightFw(self, start, end):
        print('turn right')
        self.mc.setInProg()
        self.mc.cw_motor(self.mc.motor2, start, end)
        self.mc.ccw_motor(self.mc.motor1, start, end)
        self.mc.scheTaskComplete(end)

    def poll(self):
        #print('....')
        self.mc.pollSensors()
        self.inProg = self.mc.inProg

    def cleanup(self):
        self.mc.cleanup()


class Action:
    def __init__(self):
        self.steps = []
        self.duration = 0

    def add_step(self, step, duration):
        start = self.duration
        end = start + duration
        self.duration += duration
        self.steps.append((step, start, end))

    def act(self):
        for step in self.steps:
            yield step


class ActionCoordinator:
    def __init__(self, motion_coordinator):
        self.mc = motion_coordinator

    def execute(self, cmd):
        getattr(self, cmd)()

    def back_and_forth(self, duration, times):
        action = Action()
        for i in range(times):
            action.add_step(self.mc.forward, duration)
            action.add_step(self.mc.backward, duration)
        self.act(action)

    def forward(self, duration):
        action = Action()
        action.add_step(self.mc.forward, duration)
        self.act(action)

    def forward20ms(self):
        action = Action()
        action.add_step(self.mc.forward, 0.5)
        self.act(action)

    def forwardUntil(self):
        action = Action()
        self.mc.forwardUntil()
        # action.add_step(self.mc.forward, 0.2)
        # self.act(action)

    def turnRightFwd(self):
        action = Action()
        #action.add_step(self.mc.forward, 0.2)
        action.add_step(self.mc.turnRightFw, 2)
        self.act(action)

    def turnRightFwdIndef(self):
        action = Action()
        self.mc.turnRightFwIndef()

    def forwardStart(self):
        print('Forward One Node START')

    def forwardEnd(self):
        print('Forward One Node END')

    def forwardRTurnStart(self):
        print('Forward One Node START')

    def forwardRTurnEnd(self):
        print('Forward One Node START')

    def poll(self):
        #print('...')
        self.mc.poll()

    def act(self, action):
        steps = action.act()
        while True:
            try:
                step = next(steps)  # Returns a tuple (step, start, end)
                step[0](step[1], step[2])
            except StopIteration:
                break

    def cleanup(self):
        self.mc.cleanup()


class CommandCoordinator:
    def __init__(self, action_coordinator):
        self.ac = action_coordinator
        self.act_queue = queue.Queue()
        self.inProg = False

    def execute(self, cmd):
        getattr(self, cmd)()

    def dance(self):
        print('dance')
        self.ac.back_and_forth(randint(2, 5), randint(1, 7))

    def fwdDelta(self):
        # Go forward one node
        print("Forward Delta")
        self.act_queue.put("forward20ms")  # self.ac.forward(0.2)

    def fwd1(self):
        # Go forward one node
        
        self.act_queue.put("forwardStart")
        # self.commandStart()
        # 
        self.act_queue.put("forward20ms")  # self.ac.forward(0.2)
        ## Change current position (in xml file) to in between current node and next node (Ex: Current Node = Between Prev Node & Next Node)
        self.act_queue.put("forwardUntil")  # self.ac.forwardUntil()
        ## Change current position (in xml file) to next node (Ex: Current Node = Next Node, Prev and Next node null)
        # self.act_queue.put('commandComplete') #self.commandComplete()
        self.act_queue.put("forwardEnd")

    def bck1(self):
        # Go Backward one node
        print("Backward One Node")
        # Change current position to in between current node and next node
        self.ac.backward(0.2)
        self.ac.backwardUntil()

    def fwd2(self):
        # Go forward two node
        print("Forward Two Node")
        # Change current position to in between current node and next node
        self.fwd1()
        self.fwd1()
        # self.commandComplete()

    def bck2(self):
        # Go Backward two node
        print('Backward Two Node')
        # Change current position to in between current node and next node
        self.bck1()
        self.bck1()
        self.commandComplete()

    def fwdINode(self):
        # Go forward one node
        print('Forward passing an intersection node')
        # Change current position to in between current node and next node
        self.ac.forward(0.4)
        self.ac.forwardUntil()
        self.commandComplete()

    def fwdRTurn(self):
        # Go Backward one node
        self.act_queue.put("forwardRTurnStart")
        # Change current position to in between current node and next node
        #self.fwd1()

        self.act_queue.put("turnRightFwd")
        self.act_queue.put("turnRightFwdIndef")  # self.ac.turnRightFwd()
        #self.fwd2()
        # self.commandComplete()
        self.act_queue.put('forwardRTurnEnd')

    def fwdLTurn(self):
        # Go Backward one node
        print('Making a forward left turn')
        # Change current position to in between current node and next node
        self.fwd1()
        self.fwdINode()
        self.ac.turnLeftFwd()
        self.fwd1()
        self.fwdINode()
        self.fwd2()
        self.commandComplete()

    def checkSensor(self):
        #print('Checking The Sensors...')
        self.ac.poll()
        # self.ac.back_and_forth(randint(2, 5), randint(1, 7))

    def poll(self):
        #print('Polling...')
        self.checkSensor()

    def cleanup(self):
        self.ac.cleanup()


class Robot:
    def __init__(self):
        self.cmd_queue = queue.Queue()
        self.evt_loop = asyncio.get_event_loop()
        self.cc = CommandCoordinator(ActionCoordinator(MotionCoordinator(MotorCoordinator(self.evt_loop))))
        self.speedList = [0, 55, 75, 95]
        self.gear = 3
        self.currentAct="empty"

    def command(self, cmd):
        #time.sleep(0.5)
        self.cmd_queue.put(cmd)
        print(self.cmd_queue.queue)

    def status(self):
        # JSON Generation
        gear = self.gear
        data = {}
        tempList = list(self.cc.act_queue.queue)  
        data['values'] = []  
        data['values'].append({"name":"honkhonk","gear":gear,"speed":self.speedList[self.gear],"currentAction":self.currentAct,"actionQueue":tempList
        })
        JSON = json.dumps(data, indent=4,separators=(',', ': '), ensure_ascii=False)
        return JSON

    def run(self):
        while True:
            if not self.cmd_queue.empty():
                cmd = self.cmd_queue.get()
                if cmd == 'terminate':
                    break
                else:
                    self.currentCmd=cmd
                    self.cc.execute(cmd)
            if (not self.cc.act_queue.empty()) and (not self.cc.ac.mc.inProg):
                time.sleep(0.5)  ## Sleep for testing purposes
                act = self.cc.act_queue.get()
                self.currentAct=act
                self.cc.ac.execute(act)

            self.cc.poll()

            ## Read Global Param from a file? (Like Speed and whatnot)

            ###self.gear = speed setting in xml file 
            speed = self.speedList[self.gear]

            self.evt_loop.stop()
            self.evt_loop.run_forever()
        self.cc.cleanup()


if __name__ == '__main__':
    #
    GPIO.setmode(GPIO.BCM)
    #
    speed = 100
    speedDelta=5
    robot = Robot()
    # robot.command('dance')
    
    SERVER_MAC_ADDRESS = '60:6C:66:B5:63:D1' # Aleksa bluetooth
    #SERVER_MAC_ADDRESS = '5C:F3:70:76:B6:5E' # My bluetooth

    # Start the communication with server
    carCommunication = communication.communication_thread(SERVER_MAC_ADDRESS,robot)
    carCommunication.start()

    robot.command('fwdDelta')
    # robot.command('fwd1')
    # robot.command('fwdRTurn')
    # robot.command('fwd1')
    # robot.command('fwd1')
    # robot.command('fwdRTurn')
    # robot.command('fwd1')
    # robot.command('fwd1')
    # robot.command('fwdRTurn')
    # robot.command('fwd1')
    # robot.command('fwd1')
    # robot.command('fwdRTurn')

    # robot.command('terminate')
    robot.run()