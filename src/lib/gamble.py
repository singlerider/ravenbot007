from src.lib.queries import Database
import random
import globals
import time
from threading import Thread


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
        if self.channel not in globals.channel_info:
            globals.channel_info[self.chan]["gamble"] = {
                "time": None, "users": {}, "points": 0}
        globals.channel_info[self.chan]['gamble'] = {
            "time": time.time(), "users": {
                self.user: True}, "points": points}
        self.points = globals.channel_info[self.chan]['gamble']["points"]
        self.g = Gamble(self.chan, self.user, self.points)

    def main(self):
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
        participants = globals.channel_info[self.chan]['gamble']["users"]
        winner = random.choice(list(participants.keys()))
        winner_points = self.points * (len(participants) - 1)
        completion_time = time.time()
        for participant in list(participants.keys()):
            if len(participants) > 1:  # document the outcome in the db
                if participant == winner:
                    self.g.add_gamble_database_entry(
                        self.chan, participant, int(completion_time),
                        winner_points, won=True,
                    )
                else:
                    self.g.add_gamble_database_entry(
                        self.chan, participant, int(completion_time),
                        (self.points * -1), won=False
                    )
            if participant != winner:
                self.g.apply_yield(self.chan, participant, self.points * -1)
            else:
                self.g.apply_yield(self.chan, winner, winner_points)
        win_resp = "Congratulations, {0}, you won {1} cash!".format(
            winner, winner_points)
        self.irc.send_message(self.channel, win_resp)


class Gamble:

    def __init__(self, channel="testchannel", user="testuser", points=0):
        self.db = Database()
        self.channel = channel
        self.user = user
        self.points = points

    def initiate_gamble(self):
        if self.channel not in globals.channel_info:
            globals.channel_info[self.channel]["gamble"] = {
                "time": None, "users": {}, "points": 0}
        globals.channel_info[self.channel]['gamble'] = {
            "time": time.time(), "users": {
                self.user: True}, "points": self.points}

    def terminate_gamble(self):
        globals.channel_info[self.channel]['gamble']["time"] = None

    def check_gamble(self):
        if self.channel not in globals.channel_info:
            globals.channel_info[self.channel]["gamble"] = {
                "time": None, "users": {}}
        if globals.channel_info[self.channel]['gamble']["time"]:
            return globals.channel_info[self.channel]['gamble']["time"]
        else:
            return None

    def get_gamble_user(self, chan, user):
        user_value = globals.channel_info[chan]['gamble'][
            "users"].get(user)
        if user_value:
            return True
        else:
            return False

    def rob_yield(self, multiplier=1):
        points_yield = random.choice(list(range(1, 11)))
        points = 0
        if points_yield > 9:
            points = random.choice(list(range(1, 301))) * multiplier
        elif points_yield <= 9 and points_yield > 5:
            points = random.choice(list(range(1, 21))) * multiplier
        elif points_yield <= 5 and points_yield > 1:
            points = random.choice(list(range(1, 11))) * multiplier
        else:
            points = self.points
        if bool(random.getrandbits(1)):
            points *= -1
        return points

    def apply_yield(self, channel, user, points):
        self.db.modify_points(user, channel, points)

    def add_gamble_database_entry(
            self, channel, user, timestamp, result, won=False):
        self.db.add_gamble_entry(
            user=user, channel=channel, timestamp=timestamp, result=result,
            won=won
        )
