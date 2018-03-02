import os


class Monitor:
    def on(self):
        os.system("vcgencmd display_power 1")

    def off(self):
        os.system("vcgencmd display_power 0")
