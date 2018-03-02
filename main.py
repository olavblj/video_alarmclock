import os
import time
from random import choice

from phue import Bridge

from models.alarm import Alarm
from models.button import Button
from models.button_system import ButtonSystem
from models.number_display import NumberDisplay
from models.system_state import SystemState as ss

b = Bridge('192.168.0.100')
b.connect()

system_state = ss.IDLE

alarm = None
num_display = NumberDisplay()

confirm_button = Button(16, "confirm")
up_button = Button(18, "up")
down_button = Button(12, "down")
button_system = ButtonSystem([confirm_button, up_button, down_button])

while True:
    pressed_button = button_system.poll()

    if system_state == ss.IDLE:
        if pressed_button == "confirm":
            system_state = ss.SETTING_ALARM
    elif system_state == ss.SETTING_ALARM:
        num_display.show_time()

        if pressed_button == "up":
            num_display += 30
        elif pressed_button == "down":
            num_display -= 30
        elif pressed_button == "confirm":
            system_state = ss.WAITING_ALARM
            alarm = Alarm(num_display.display_time, hue_bridge=b)
            alarm.start()
            num_display.turn_off()

    elif system_state == ss.WAITING_ALARM:
        if pressed_button == "confirm":
            system_state = ss.SETTING_ALARM

        if alarm.has_run:
            system_state = ss.RUNNING_ALARM
    elif system_state == ss.RUNNING_ALARM:
        pass
    else:
        print("State not handled")
