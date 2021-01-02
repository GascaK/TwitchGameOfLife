import RPi.GPIO as GPIO

class RaspPi():
    def __init__(self):
        self.commands = ['WATER', 'FOOD', 'LIGHTS', 'CAMERA']
        GPIO.setmode(GPIO.BOARD)

    def command_list(self, command):
        if command == "WATER":
            print("Watering ants.")
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

    def cm_water(self, time):
        led = 17
        GPIO.setup(led, GPIO.OUT)
        for i in range(time):
            GPIO.output(led, GPIO.HIGH)
            time.sleep(.2)
            GPIO.output(led, GPIO.LOW)
            time.sleep(.2)

''' getting the pi setup standby '''