import RPi.GPIO as GPIO
import time


class NumberDisplay:
    # @formatter:off
    pin_map = {
        1: 2,
        2: 3,
        3: 4,
        4: 17,
        5: 27,
        6: 22,
        7: 26,
        8: 19,
        9: 13,
        10: 6,
        11: 5,
        12: 12
    }

    num_map = {
        ' ': (0, 0, 0, 0, 0, 0, 0),
        '0': (1, 1, 1, 1, 1, 1, 0),
        '1': (0, 1, 1, 0, 0, 0, 0),
        '2': (1, 1, 0, 1, 1, 0, 1),
        '3': (1, 1, 1, 1, 0, 0, 1),
        '4': (0, 1, 1, 0, 0, 1, 1),
        '5': (1, 0, 1, 1, 0, 1, 1),
        '6': (1, 0, 1, 1, 1, 1, 1),
        '7': (1, 1, 1, 0, 0, 0, 0),
        '8': (1, 1, 1, 1, 1, 1, 1),
        '9': (1, 1, 1, 1, 0, 1, 1)
    }
    # @formatter:on

    digits = [12, 9, 8, 6]
    segments = [1, 2, 4, 5, 7, 10, 11]
    dot = 3

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarning(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    def set_digit(self, digit_index, digit_value):
        try:
            for i, segment in enumerate(self.segments):
                GPIO.output(self.pin_map[segment], self.num_map[digit_value][i])
        except KeyboardInterrupt:

    def set_time_of_day(self, time_of_day="9:30"):
        if ":" in time_of_day and len(time_of_day) == any([3, 4]):
            time_of_day = time_of_day.replace(":", "")
            if len(time_of_day) == 3:
                time_of_day = "0" + time_of_day

            for i, digit_val in enumerate(time_of_day):
                self.set_digit(i, digit_val)

        else:
            print("Invalid time_of_day input")

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()


import sys


def setup_system(time_of_day):
    num_display = NumberDisplay()

    num_display.set_digit(0, "0")
    time.sleep(3)

    num_display.set_time_of_day(time_of_day)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    setup_system(argv[1])


if __name__ == "__main__":
    main()
