import time

import RPi.GPIO as GPIO
from phue import Bridge

from models.alarm import Alarm
from models.button import Button
from models.button_system import ButtonSystem
from models.number_display import NumberDisplay
from models.system_state import SystemState as ss
from singletons.monitor import Monitor
from singletons.light_system import LightSystem
from utils import config

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

monitor = Monitor()
light_sys = LightSystem()

system_state = ss.IDLE

alarm = None
num_display = NumberDisplay()

confirm_button = Button(16, "confirm", cooldown=1)
up_button = Button(18, "up")
down_button = Button(12, "down")

light_button = Button(22, "light")

button_system = ButtonSystem([confirm_button, up_button, down_button, light_button])

monitor.on()

try:
    while True:
        pressed_button = button_system.poll()

        # <--- STATE INDEPENDENT --->
        if pressed_button == "light":
            light_sys.toggle()

        # <--- IDLE --->
        if system_state == ss.IDLE:
            monitor.on()
            if pressed_button == "confirm":
                system_state = ss.SETTING_ALARM

        # <--- SETTING_ALARM --->
        elif system_state == ss.SETTING_ALARM:
            num_display.show_time()
            monitor.on()
            if pressed_button == "up":
                num_display += config.set_alarm_incr
            elif pressed_button == "down":
                num_display -= config.set_alarm_incr
            elif pressed_button == "confirm":
                system_state = ss.WAITING_ALARM
                alarm = Alarm(str(num_display))
                alarm.start()
                num_display.turn_off()

        # <--- WAITING_ALARM --->
        elif system_state == ss.WAITING_ALARM:
            monitor.off()
            if pressed_button == "confirm":
                system_state = ss.SETTING_ALARM
            if alarm.ring_time is not None:
                system_state = ss.RUNNING_ALARM

        # <--- RUNNING_ALARM --->
        elif system_state == ss.RUNNING_ALARM:
            monitor.on()

            if time.time() - alarm.ring_time > 30 * 60:
                alarm.abort()
                system_state = ss.IDLE

        else:
            print("State not handled")

except:
    if alarm is not None:
        alarm.abort()
