from src.lib.twitch import *
from src.lib.queries import Database

TEST_USER = "singlerider"


class Cash:
    def __init__(self, channel):
        self.db = Database()
        self.channel = channel

    def add_all(self, points):
        user_dict, all_users = get_dict_for_users(self.channel)
        self.db.add_user(all_users, self.channel)
        for user in all_users:
            self.db.modify_points([user], self.channel, points)
        return {"users": all_users, "channel": self.channel, "points": points}

    def add(self, users, points):
        self.db.add_user(users, self.channel)
        self.db.modify_points(users[0], self.channel, points)
        return {"user": users[0], "channel": self.channel, "points": points}

    def modify(self, users, points):
        self.db.add_user(users, self.channel)
        self.db.modify_points(users[0], self.channel, points)
        return {"user": users[0], "channel": self.channel, "points": points}

    def get(self, user):
        # (3, u'testuser', 5, u'mod')
        user_data = self.db.get_user(user, self.channel)
        if user_data:
            return {
                "user": user_data[1], "channel": self.channel,
                "points": user_data[2]
                }
        else:
            return {"user": user, "channel": self.channel, "points": 0}


def cron(channel):
    c = Cash(channel)
    points_added_to = c.add_all(channel, 1)
    print "performed points cron"


def cash(args):
    c = Cash(globals.global_channel)
    if len(args) < 1:
        user = globals.CURRENT_USER
        points = c.get(user)["points"]
        return str(points) + " (note - this cash is subject to removal " + \
            "during this early development cycle) - singlerider"
    if len(args[0].split(" ")) == 1:
        user = args[0].lower()
        points = c.get(user)["points"]
        return str(points)
    else:
        user_dict, all_users = get_dict_for_users()
        args = args[0].split(" ")
        action = args[0].lower()
        user = args[1].lower()
        if globals.CURRENT_USER not in user_dict["chatters"]["moderators"]:
            if globals.CURRENT_USER != TEST_USER:
                return "This is a moderator-only command"
        try:
            delta = int(args[2])
        except:
            return "The third keyword must be a number"
        if action == "add" or action == "remove" or action == "set":
            if action == "add":
                if user == "all":
                    if len(all_users) < 1:
                        return "Twitch's backend appears to be down"
                    for user in all_users:
                        c.modify([user], delta)
                    return "Added {0} cash to {1} Conspirators".format(
                        delta, len(all_users))
                else:
                    c.modify([user], abs(delta))
                    return "Added {0} cash to {1}".format(delta, user)
            elif action == "remove":
                c.modify([user], abs(delta) * -1)
                return "Removed {0} cash from {1}".format(delta, user)
            elif action == "set":
                return "This one is still in progress"
        else:
            return "The first keyword must be either 'add', 'remove', or 'set'"
