import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setwarning(False)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


