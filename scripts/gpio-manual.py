import time
import RPi.GPIO as gpio
def run(attr):
    print(attr)
    attr_array = attr.split("//")
    print(attr_array)
    if(attr_array[1] == "on"):
        gpio.setmode(gpio.BCM)
        gpio.setup(int(attr_array[0]), gpio.HIGH)
    elif(attr_array[1] == "off"):
        gpio.setmode(gpio.BCM)
        gpio.setup(int(attr_array[0]), gpio.LOW)
