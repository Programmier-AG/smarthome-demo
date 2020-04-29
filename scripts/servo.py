import RPi.GPIO as GPIO
import time

def run(attr):
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
    p.start(2.5) # Initialisierung

    try:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.stop()
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
