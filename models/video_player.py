import os
import threading


class VideoPlayer(threading.Thread):
    def __init__(self, video_fp):
        threading.Thread.__init__(self)
        self.fp = video_fp
        self.video_finished = False

    def run(self):
        os.system("omxplayer {}".format(self.fp))
        self.video_finished = True
