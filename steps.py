'''
    Stepper Motor interfacing with Raspberry Pi
    http:///www.electronicwings.com
'''
import RPi.GPIO as GPIO
from time import sleep
import sys
class MySteps():
    def __init__(self):
        self.motor_channel = (11,13,15,19)  
#assign GPIO pins for motor

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
    #for defining more than 1 GPIO channel as input/output use
        GPIO.setup(self.motor_channel, GPIO.OUT)
    def rotate(self,motor_direction): # c for clockwise & a for anti-clockwise
        for i in range(0,201):
            if(motor_direction == 'c'): 
                print('motor running clockwise\n')
                GPIO.output(self.motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                sleep(0.002)
                

            elif(motor_direction == 'a'):
                print('motor running anti-clockwise\n')
                GPIO.output(self.motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                sleep(0.002)
                GPIO.output(self.motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                sleep(0.002)
        print('Rotation Complete')
    


