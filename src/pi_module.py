import RPi.GPIO as GPIO
import time

class RaspPi():
    def __init__(self, warning = False):
        self.commands = ['WATER', 'FOOD', 'LIGHTS', 'CAMERA']
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(warning)

    def command_list(self, command):
        if command == "WATER":
            print("Watering ants.")
            cm_water(5)
        elif command == "FOOD":
            print("Feeding ants.")
        elif command == "LIGHT":
            print("Changing lights.")
        elif command == "CAMERA":
            print("Changing camera.")
        else:
            print("Command not implemented.")

    def get_commands(self):
        ''' Get commands list.'''
        return self.commands

    def cm_water(self, count):
        led = 17
        GPIO.setup(led, GPIO.OUT)
        for i in range(time):
            GPIO.output(led, GPIO.HIGH)
            time.sleep(.2)
            GPIO.output(led, GPIO.LOW)
            time.sleep(.2)