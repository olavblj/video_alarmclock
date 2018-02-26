import os, sys, time
from random import choice

from test_display import NumberDisplay


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


def main(argv=None):
    if argv is None:
        argv = sys.argv

    num_display = NumberDisplay()

    while not num_display.is_confirmed:
        num_display.poll_buttons()
        num_display.show_time()

    print(num_display.display_time_string())

    # set_alarm(num_display.display_time_string())


if __name__ == "__main__":
    main()
