import RPi.GPIO as GPIO
import time
import datetime

# @formatter:off

pin_map = {
    1: 3,
    2: 5,
    3: 7,
    4: 11,
    5: 13,
    6: 15,
    7: 37,
    8: 35,
    9: 33,
    10: 31,
    11: 32,
    12: 29
}

digit_map = {
    " ": [],
    "0": [1, 2, 4, 7, 11, 10],
    "1": [4, 7],
    "2": [11, 7, 5, 1, 2],
    "3": [11, 7, 5, 4, 2],
    "4": [10, 5, 7, 4],
    "5": [11, 10, 5, 4, 2],
    "6": [11, 10, 1, 2, 4, 5],
    "7": [11, 7, 4],
    "8": [11, 10, 5, 7, 1, 2, 4],
    "9": [11, 10, 5, 7, 2, 4]
}

# @formatter:on


class NumberDisplay:
    # <--- OUTPUT PINS --->
    digits = [29, 33, 35, 15]
    segments = [3, 5, 11, 13, 37, 31, 32]
    dot = 7

    # <--- INPUT PINS --->
    up_pin = 18
    down_pin = 12
    confirm_pin = 16

    def __init__(self):
        self.is_confirmed = False
        self.last_button_press = time.time()
        self.display_time = datetime.time(hour=9, minute=0)

        self.num_map = {key: [0 if segment in [pin_map[val] for val in value] else 1 for segment in self.segments] for
                        (key, value) in digit_map.items()}

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)

        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

        GPIO.setup(self.dot, GPIO.OUT)
        GPIO.output(self.dot, 1)

        GPIO.setup(self.up_pin, GPIO.IN)
        GPIO.setup(self.down_pin, GPIO.IN)
        GPIO.setup(self.confirm_pin, GPIO.IN)

    def set_digit(self, digit_index, digit_value):
        for i, segment in enumerate(self.segments):
            GPIO.output(segment, self.num_map[digit_value][i])

        GPIO.output(self.dot, 0 if digit_index == 1 else 1)

        GPIO.output(self.digits[digit_index], 1)
        time.sleep(0.001)
        GPIO.output(self.digits[digit_index], 0)

    def show_time(self):
        time_string = str(self)
        time_string = time_string.replace(":", "")
        if len(time_string) == 3:
            time_string = "0" + time_string

        for i, digit_val in enumerate(time_string):
            self.set_digit(i, digit_val)

    def __iadd__(self, other):
        self.display_time = time_plus(self.display_time, datetime.timedelta(minutes=other))
        return self

    def __isub__(self, other):
        self.display_time = time_plus(self.display_time, datetime.timedelta(minutes=-other))
        return self

    def __str__(self):
        return self.display_time.strftime('%H:%M')

    def poll_buttons(self):
        if time.time() - self.last_button_press > 0.2:
            if not GPIO.input(self.up_pin):
                self.last_button_press = time.time()
                self.display_time = time_plus(self.display_time, datetime.timedelta(minutes=30))

            elif not GPIO.input(self.down_pin):
                self.last_button_press = time.time()
                self.display_time = time_plus(self.display_time, datetime.timedelta(minutes=-30))

            elif not GPIO.input(self.confirm_pin):
                self.last_button_press = time.time()
                self.is_confirmed = True

    def turn_off(self):
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 0)

        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)

        GPIO.setup(self.dot, GPIO.OUT)
        GPIO.output(self.dot, 1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.turn_off()
        GPIO.cleanup()


def time_plus(time, timedelta):
    start = datetime.datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()
