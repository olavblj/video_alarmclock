import time
import RPi.GPIO as GPIO


class Button:
    def __init__(self, pin_number, name, cooldown=0.2):
        self.pin_number = pin_number
        self.last_press = time.time()
        self.cooldown = cooldown

        GPIO.setup(self.pin_number, GPIO.IN)

    def poll(self):
        if time.time() - self.last_press > self.cooldown:
            if not GPIO.input(self.pin_number):
                self.last_press = time.time()
                return True

        return False
