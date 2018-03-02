import os
import random
import threading
import time

from models.video_player import VideoPlayer
from utils import config


class Alarm(threading.Thread):
    def __init__(self, alarm_time, hue_bridge=None):
        threading.Thread.__init__(self)
        self.alarm_time = alarm_time
        self.hue_bridge = hue_bridge
        self.ring_time = None
        self.aborted = False

    def run(self):
        ctime = time.strftime("%H:%M")
        while ctime != self.alarm_time and not self.aborted:
            ctime = time.strftime("%H:%M")
            print("[Alarm] {} - {}".format(ctime, self.alarm_time))
            time.sleep(1)

        print("[Alarm] Play episode")
        self.alarm_ring()

    def abort(self):
        self.aborted = True

    def alarm_ring(self):
        self.ring_time = time.time()
        time.sleep(5)

        all_episodes = os.listdir("episodes")

        chosen_episode_fp = "episodes/{}".format(random.choice(all_episodes))

        VideoPlayer(chosen_episode_fp).start()

        time.sleep(60 * config.light_on_delay)

        if self.hue_bridge is not None:
            lights = self.hue_bridge.lights
            command = {'transitiontime': 600 * config.light_on_transition, 'on': True, 'bri': 254}

            for light in lights:
                self.hue_bridge.set_light(light.light_id, command)
