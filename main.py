import os, sys, time
from random import choice


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

    set_alarm(argv[1])


if __name__ == "__main__":
    main()
