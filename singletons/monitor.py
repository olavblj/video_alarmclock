import os


class Monitor:
    class __Monitor:
        def __init__(self, is_on=None):
            self.is_on = is_on

        def on(self):
            if self.is_on is not True:
                self.is_on = True
                os.system("vcgencmd display_power 1")

        def off(self):
            if self.is_on is not False:
                self.is_on = False
                os.system("vcgencmd display_power 0")

    instance = None

    def __init__(self):
        if not Monitor.instance:
            Monitor.instance = Monitor.__Monitor()

    def __getattr__(self, name):
        return getattr(self.instance, name)
