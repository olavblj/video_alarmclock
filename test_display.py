import RPi.GPIO as GPIO
import time
import datetime


class NumberDisplay:
    # @formatter:off

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

    # <--- OUTPUT PINS --->
    digits = [29, 33, 35, 15]
    segments = [3, 5, 11, 13, 37, 31, 32]
    dot = 7

    # <--- INPUT PINS --->
    up_pin = 18
    down_pin = 12
    confirm_pin = 16

    def __init__(self):
        self.time_of_day = datetime.time(hour=9, minute=0)

        self.num_map = {key: [0 if segment in value else 1 for segment in self.segments] for (key, value) in
                        self.digit_map.items()}

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for segment in self.segments:
            print("Segment: {}".format(segment))
            print("Mapped segment: {}".format(segment))

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
        time_string = self.time_of_day.strftime('%H:%M')
        if ":" in time_string and (4 <= len(time_string) <= 5):
            time_string = time_string.replace(":", "")
            if len(time_string) == 3:
                time_string = "0" + time_string

            for i, digit_val in enumerate(time_string):
                self.set_digit(i, digit_val)
        else:
            print("Invalid time_of_day input: {}".format(time_string))

    def poll_buttons(self):
        if not GPIO.input(self.up_pin):
            self.time_of_day += datetime.timedelta(minutes=30)

        elif not GPIO.input(self.down_pin):
            self.time_of_day -= datetime.timedelta(minutes=30)

        elif not GPIO.input(self.confirm_pin):
            print("Confirmed!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()


import sys


def setup_system():
    num_display = NumberDisplay()

    alarm_time = datetime.time(hour=9, minute=0)

    while True:
        num_display.poll_buttons()
        num_display.show_time()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    setup_system()


if __name__ == "__main__":
    main()
