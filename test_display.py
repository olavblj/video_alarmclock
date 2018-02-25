import RPi.GPIO as GPIO
import time


class NumberDisplay:
    # @formatter:off
    pin_map = {
        1: 18,
        2: 23,
        3: 24,
        4: 25,
        5: 8,
        6: 7,
        7: 26,
        8: 19,
        9: 13,
        10: 6,
        11: 5,
        12: 12
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

    digits = [12, 9, 8, 6]
    segments = [1, 2, 4, 5, 7, 10, 11]
    dot = 3

    def __init__(self):
        self.num_map = {key: [0 if segment in value else 1 for segment in self.segments] for (key, value) in
                        self.digit_map.items()}

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for segment in self.segments:
            print("Segment: {}".format(segment))
            print("Mapped segment: {}".format(self.pin_map[segment]))

            GPIO.setup(self.pin_map[segment], GPIO.OUT)
            GPIO.output(self.pin_map[segment], 0)

        for digit in self.digits:
            GPIO.setup(self.pin_map[digit], GPIO.OUT)
            GPIO.output(self.pin_map[digit], 1)

        GPIO.setup(self.pin_map[self.dot], GPIO.OUT)
        GPIO.output(self.pin_map[self.dot], 0)

    def set_digit(self, digit_index, digit_value):
        for i, digit in enumerate(self.digits):
            if i == digit_index:
                GPIO.output(self.pin_map[digit], 1)
            else:
                GPIO.output(self.pin_map[digit], 0)

        for i, segment in enumerate(self.segments):
            GPIO.output(self.pin_map[segment], self.num_map[digit_value][i])

    def set_time_of_day(self, time_of_day="9:30"):
        if ":" in time_of_day and (4 <= len(time_of_day) <= 5):

            while True:
                time_of_day = time_of_day.replace(":", "")
                if len(time_of_day) == 3:
                    time_of_day = "0" + time_of_day

                for i, digit_val in enumerate(time_of_day):
                    self.set_digit(i, digit_val)
        else:
            print("Invalid time_of_day input: {}".format(time_of_day))

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()


import sys


def setup_system(time_of_day):
    num_display = NumberDisplay()

    num_display.set_time_of_day(time_of_day)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    setup_system(argv[1])


if __name__ == "__main__":
    main()
