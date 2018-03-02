import os
import random
import threading
import time

from models.video_player import VideoPlayer


class Alarm(threading.Thread):
    def __init__(self, alarm_time, hue_bridge=None):
        threading.Thread.__init__(self)
        self.alarm_time = alarm_time
        self.hue_bridge = hue_bridge
        self.has_run = False

    def run(self):
        ctime = time.strftime("%H:%M")
        print(ctime)

        while ctime != self.alarm_time:
            ctime = time.strftime("%H:%M")
            print("[Alarm] {} - {}".format(ctime, self.alarm_time))
            time.sleep(1)

        print("[Alarm] Play episode")
        self.alarm_ring()

    def alarm_ring(self):
        self.has_run = True
        time.sleep(5)

        all_episodes = os.listdir("episodes")

        chosen_episode_fp = "episodes/{}".format(random.choice(all_episodes))

        VideoPlayer(chosen_episode_fp).start()

        time.sleep(60 * 1)

        if self.hue_bridge is not None:
            lights = self.hue_bridge.lights
            command = {'transitiontime': 100, 'on': True, 'bri': 254}

            for light in lights:
                self.hue_bridge.set_light(light.light_id, command)