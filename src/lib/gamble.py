from src.lib.queries import Database
import random
import globals
import time
from threading import Thread
import sys


def initialize(channel, user, delay, points):
    GambleThread(globals.irc, channel, delay, user, points).start()


class GambleThread(Thread):

    def __init__(self, irc, channel, delay, user, points):
        Thread.__init__(self, target=self.main)
        self.daemon = True
        self.delay = delay
        self.now = time.time()
        self.channel = "#" + channel.lstrip("#")
        self.chan = channel
        self.irc = irc
        self.user = user
        self.points = points
        self.g = Gamble(self.chan, self.user, self.points)

    def main(self):
        chan = self.channel.lstrip("#")
        begin_resp = "Gambling has begun!"
        end_resp = "Gambling has finished!"
        time_left = "{0} seconds of gambling remain!".format(self.delay / 2)
        self.g.initiate_gamble()
        self.irc.send_message(self.channel, begin_resp)
        time.sleep(float(self.delay / 2))
        self.irc.send_message(self.channel, time_left)
        time.sleep(float(self.delay / 2))
        self.g.terminate_gamble()
        self.irc.send_message(self.channel, end_resp)
        for user in globals.channel_info[self.chan]['gamble']["users"]:
            points = self.g.rob_yield(multiplier=1)
            self.g.apply_yield(self.chan, user, points)
        sys.exit()


class Gamble:

    def __init__(self, channel="testchannel", user="testuser", points=0):
        self.db = Database()
        self.channel = channel
        self.user = user
        self.points = points

    def initiate_gamble(self):
        if self.channel not in globals.channel_info:
            globals.channel_info[self.channel]["gamble"] = {
                "time": None, "users": {}}
        globals.channel_info[self.channel]['gamble'] = {
            "time": time.time(), "users": {self.user: self.points}}

    def terminate_gamble(self):
        globals.channel_info[self.channel]['gamble']["time"] = None

    def check_gamble(self):
        if self.channel not in globals.channel_info:
            print globals.channel_info
            globals.channel_info[self.channel]["gamble"] = {
                "time": None, "users": {}}
        if globals.channel_info[self.channel]['gamble']["time"]:
            return globals.channel_info[self.channel]['gamble']["time"]
        else:
            return None

    def rob_yield(self, multiplier=1):
        points_yield = random.choice(range(1, 11)) * multiplier
        points = 0
        if points_yield > 9:
            points = random.choice(range(1, 301))
        elif points_yield <= 9 and points_yield > 5:
            points = random.choice(range(1, 21))
        elif points_yield <= 5 and points_yield > 1:
            points = random.choice(range(1, 11))
        else:
            points = self.points
        if bool(random.getrandbits(1)):
            points *= -1
        return points

    def apply_yield(self, channel, user, points):
        self.db.modify_points(user, points)
