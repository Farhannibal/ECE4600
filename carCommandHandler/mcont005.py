import RPi.GPIO as GPIO
#import bluetooth
import asyncio
from random import randint
import queue

class Motor:
    def __init__(self, en_pin, in_pin, out_pin):
        self.en_pin = en_pin
        self.in_pin = in_pin
        self.out_pin = out_pin

        self.pwm = None

    def setup(self, freq, dc):
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.setup(self.in_pin, GPIO.OUT)
        GPIO.setup(self.out_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.en_pin, freq)
        self.pwm.start(dc)

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


    # ToDo: Add IR Sensor to adjust speed
    #
    #
    #

    def cleanup(self):
        self.pwm.stop()


class MotorCoordinator:
    FREQ = 500

    EN1 = 26
    I1 = 2
    O1 = 3
    DC1 = 90

    EN2 = 13
    I2 = 17
    O2 = 27
    DC2 = 90

    def __init__(self, evt_loop):
        self.evt_loop = evt_loop
        self.motor1 = Motor(self.EN1, self.I1, self.O1)
        self.motor2 = Motor(self.EN2, self.I2, self.O2)

        self.motor1.setup(self.FREQ, self.DC1)
        self.motor2.setup(self.FREQ, self.DC2)

    def cw_motor(self, motor, start, end):
        #print('cw_motor')
        self.schedule(motor.cw, start)
        self.schedule(motor.stop, end)

    def ccw_motor(self, motor, start, end):
        self.schedule(motor.ccw, start)
        self.schedule(motor.stop, end)

    def schedule(self, func, delay):
        #print('schedule')
        self.evt_loop.call_later(delay, func)

    def cleanup(self):
        self.motor1.cleanup()
        self.motor2.cleanup()
        GPIO.cleanup()


class MotionCoordinator:
    def __init__(self, motor_coordinator):
        self.mc = motor_coordinator

    def forward(self, start, end):
        #print('forward')
        self.mc.cw_motor(self.mc.motor1, start, end)
        self.mc.cw_motor(self.mc.motor2, start, end)

    def backward(self, start, end):
        self.mc.ccw_motor(self.mc.motor1, start, end)
        self.mc.ccw_motor(self.mc.motor2, start, end)

    def turnRightFw(self):
        self.mc.cw_motor(self.mc.motor1, start, end)

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

    def back_and_forth(self, duration, times):
        action = Action()
        for i in range(times):
            action.add_step(self.mc.forward, duration)
            action.add_step(self.mc.backward, duration)
        self.act(action)

    def forward(self,duration):
        action = Action()
        action.add_step(self.mc.forward, duration)
        self.act(action)

    def turnRightFw(self):
        action = Action()
        action.add_step(self.mc.forward, 0.2)
        action.add_step(self.mc.turnRightFw, 1)
        self.act(action)


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

    def execute(self, cmd):
        getattr(self, cmd)()

    def dance(self):
        print('dance')
        self.ac.back_and_forth(randint(2, 5), randint(1, 7))

    def checkSensor(self):
        print('Checking The Sensors')
        #self.ac.back_and_forth(randint(2, 5), randint(1, 7))        

    def cleanup(self):
        self.ac.cleanup()


class Robot:
    def __init__(self):
        self.cmd_queue = queue.Queue()
        self.evt_loop = asyncio.get_event_loop()
        self.cc = CommandCoordinator(ActionCoordinator(MotionCoordinator(MotorCoordinator(self.evt_loop))))

    def command(self, cmd):
        self.cmd_queue.put(cmd)

    def run(self):
        while True:
            if not self.cmd_queue.empty():
                cmd = self.cmd_queue.get()
                if cmd == 'terminate':
                    break
                else:
                    self.cc.execute(cmd)
            self.evt_loop.stop()
            self.evt_loop.run_forever()
        self.cc.cleanup()


if __name__ == '__main__':
    #
    GPIO.setmode(GPIO.BCM)
    #
    robot = Robot()
    robot.command('dance')

    #robot.command('terminate')
    robot.run()
