import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from transitions import Machine

from RPIO import PWM

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

value = 0

servo = PWM.Servo()

#drive
servo1Pin = 26

#steer
servo2Pin = 13


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)

forward = 1800
reverse = 1000
stop = 1390

left = 2400
right = 540
straight = 1390

sleep = time.sleep

class Rc:
    states =['tooFar','far', 'near', 'close', 'tooClose']

    def __init__(self):

        self.state1 = False

        self.state2 = False

        self.state3 = False

        self.state4 = False

        self.state5 = False

        self.machine = Machine(model=self, states=Rc.states, initial='toofar')
        self.machine.add_transition(trigger='sensorTooFar',source='*',dest='tooFar')
        self.machine.add_transition(trigger='sensorFar',source='*',dest='far')
        self.machine.add_transition(trigger='sensorNear',source='*',dest='near')
        self.machine.add_transition(trigger='sensorClose',source='*',dest='close')
        self.machine.add_transition(trigger='sensorTooClose',source='*',dest='tooClose')


    def sonar(self, sValue):

        self.value = sValue

        if (self.value <= 1023 and self.value >= 100):
            self.state1 = True
        else:
            self.state1 = False

        if (self.value <= 100 and self.value >= 70):
            self.state2= True
        else:
            self.state2= False

        if (self.value <= 70 and self.value >= 50):
            self.state3= True
        else:
            self.state3= False

        if (self.value <= 50 and self.value >= 40):
            self.state4= True
        else:
            self.state4= False

        if (self.value <= 40 and self.value >= 0):
            self.state5= True
        else:
            self.state5= False



        print (self.value)

        print self.state1

        print self.state2

        print self.state3

        print self.state4

        print self.state5

    def setState(self):
        if self.state1 == True:
            self.sensorTooFar()

        if self.state2 == True:
            self.sensorFar()

        if self.state3 == True:
            self.sensorNear()

        if self.state4 == True:
            self.sensorClose()

        if self.state5 == True:
            self.sensorTooClose()        


    def update(self):
        if self.state == "tooClose":
            GPIO.output(4,GPIO.HIGH)
            GPIO.output(17,GPIO.HIGH)
            GPIO.output(27,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(10,GPIO.HIGH)

            servo.set_servo(servo2Pin, straight)
            
            servo.set_servo(servo1Pin, reverse)

            sleep(.5)
            
            servo.stop_servo(servo1Pin)
            servo.stop_servo(servo2Pin)

            
        if self.state == "close":
            GPIO.output(4,GPIO.LOW)
            GPIO.output(17,GPIO.HIGH)
            GPIO.output(27,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(10,GPIO.HIGH)

            servo.set_servo(servo2Pin, straight)
            servo.set_servo(servo1Pin, reverse)

            sleep(.5)
            
            servo.stop_servo(servo1Pin)
            servo.stop_servo(servo2Pin)
            
        if self.state == "near":
            GPIO.output(4,GPIO.LOW)
            GPIO.output(17,GPIO.LOW)
            GPIO.output(27,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(10,GPIO.HIGH)

            servo.set_servo(servo1Pin, stop)
            sleep(1)

            servo.set_servo(servo2Pin, left)
            sleep(2)
            servo.set_servo(servo1Pin, reverse)
            sleep(1)
            servo.set_servo(servo1Pin, stop)
            sleep(1)
            servo.set_servo(servo2Pin, right)
            sleep(2)
            servo.set_servo(servo1Pin, forward)
            sleep(1)
            servo.set_servo(servo1Pin, stop)
            sleep(1)
            servo.set_servo(servo2Pin, straight)
            sleep(1)

            servo.stop_servo(servo1Pin)
            servo.stop_servo(servo2Pin)
            

            
        if self.state == "far":
            GPIO.output(4,GPIO.LOW)
            GPIO.output(17,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(10,GPIO.HIGH)

            servo.set_servo(servo2Pin, straight)
            
            servo.set_servo(servo1Pin, forward)

            sleep(.5)
            
            servo.stop_servo(servo1Pin)
            servo.stop_servo(servo2Pin)


        if self.state == "tooFar":
            GPIO.output(4,GPIO.LOW)
            GPIO.output(17,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(10,GPIO.HIGH)

            servo.set_servo(servo2Pin, straight)
            
            servo.set_servo(servo1Pin, forward)

            sleep(.5)

            servo.stop_servo(servo1Pin)
            servo.stop_servo(servo2Pin)

            




rcCar = Rc()



while True:

    sensor = mcp.read_adc(0)

    rcCar.sonar(sensor)


    rcCar.setState()

    rcCar.update()

    sleep(0.2)



    print rcCar.state

    #time.sleep(0.2)
