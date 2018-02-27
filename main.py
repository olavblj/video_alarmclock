import os, sys, time
from random import choice

from test_display import NumberDisplay
from phue import Bridge

b = Bridge('192.168.0.100')
b.connect()


def set_alarm(alarm_time):
    ctime = time.strftime("%H:%M")
    print(ctime)

    os.system("vcgencmd display_power 0")

    while ctime != alarm_time:
        ctime = time.strftime("%H:%M")
        print("{} - {}".format(ctime, alarm_time))
        time.sleep(1)

    print("Play episode")
    run_alarm()


def run_alarm():
    os.system("vcgencmd display_power 1")
    time.sleep(5)

    all_episodes = os.listdir("episodes")

    chosen_episode = choice(all_episodes)

    os.system("omxplayer episodes/{}".format(chosen_episode))
    time.sleep(600)

    lights = b.lights
    command = {'transitiontime': 3000, 'on': True, 'bri': 254}

    for light in lights:
        b.set_light(light.light_id, command)

    main()


def main():
    num_display = NumberDisplay()

    while not num_display.is_confirmed:
        num_display.poll_buttons()
        num_display.show_time()

    print(num_display.display_time_string())

    set_alarm(num_display.display_time_string())


if __name__ == "__main__":
    main()
