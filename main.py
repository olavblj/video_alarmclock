import os
import time
from random import choice

from phue import Bridge

from models.monitor import Monitor
from models.alarm import Alarm
from models.button import Button
from models.button_system import ButtonSystem
from models.number_display import NumberDisplay
from models.system_state import SystemState as ss
from system_manager import SystemManager
from utils import config

monitor = Monitor()

b = Bridge('192.168.0.100')
b.connect()

system_state = ss.IDLE

alarm = None
num_display = NumberDisplay()

confirm_button = Button(16, "confirm", cooldown=1)
up_button = Button(18, "up")
down_button = Button(12, "down")
button_system = ButtonSystem([confirm_button, up_button, down_button])

monitor.on()

try:
    while True:
        pressed_button = button_system.poll()

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
                alarm = Alarm(str(num_display), hue_bridge=b)
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
