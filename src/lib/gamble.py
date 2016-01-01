from src.lib.queries import Database
import random
import globals
import time
from threading import Thread
import sys


def initialize(channel, delay):
    GambleThread(globals.irc, channel, delay).start()


class GambleThread(Thread):

    def __init__(self, irc, channel, delay):
        Thread.__init__(self, target=self.main)
        self.daemon = True
        self.delay = delay
        self.now = time.time()
        self.channel = "#" + channel.lstrip("#")
        self.chan = channel
        self.irc = irc

    def main(self):
        chan = self.channel.lstrip("#")
        g = Gamble(self.chan)
        g.initiate_gamble()
        begin_resp = "Gambling has begun!"
        end_resp = "Gambling has finished!"
        self.irc.send_message(self.channel, begin_resp)
        time.sleep(self.delay)
        self.irc.send_message(self.channel, end_resp)
        g.terminate_gamble()
        sys.exit()


class Gamble:

    def __init__(self, channel="testchannel"):
        self.db = Database()
        self.channel = channel

    def gamble_timer(self):
        pass

    def initiate_gamble(self):
        if self.channel not in globals.channel_info:
            globals.channel_info[self.channel] = {"gamble": None}
        globals.channel_info[self.channel]['gamble'] = time.time()

    def terminate_gamble(self):
        globals.channel_info[self.channel]['gamble'] = None

    def check_gamble(self):
        if self.channel not in globals.channel_info:
            globals.channel_info[self.channel] = {"gamble": None}
        if globals.channel_info[self.channel]['gamble']:
            return globals.channel_info[self.channel]['gamble']
        else:
            return None

    def rob_yield(self, multiplier=1):
        points_yield = random.choice(range(1, 11)) * multiplier
        points = 0
        if points_yield > 9:
            points = random.choice(range(1, 301))
        elif points_yield <= 9 and points_yield > 5:
            points = random.choice(range(1, 21))
        else:
            points = random.choice(range(1, 11))
        return points
