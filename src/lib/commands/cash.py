from src.lib.twitch import *
from src.lib.queries import Database


class Cash:
    def __init__(self):
        self.db = Database()

    def add_all(self, channel, points):
        user_dict, all_users = get_dict_for_users(channel)
        self.db.add_user(all_users)
        for user in all_users:
            self.db.modify_points([user], points)
        print "added points to {0}".format(users)
        return {"users": all_users, "points": points}

    def add(self, users, points):
        self.db.add_user(users)
        self.db.modify_points(users[0], points)
        print "added {0} points to {1}".format(points)
        return {"user": users[0], "points": points}

    def modify(self, users, points):
        self.db.add_user(users)
        self.db.modify_points(users[0], points)
        print "modified {0}'s points by {1}".format(users[0], points)
        return {"user": users[0], "points": points}

    def get(self, user):
        # (3, u'testuser', 5, u'mod')
        user_data = self.db.get_user(user)
        if user_data:
            return {"user": user_data[1], "points": user_data[2]}
        else:
            return {"user": user, "points": 0}


def cron(channel):
    c = Cash()
    points_added_to = c.add_all(channel, 1)
    print "performed points cron"


def cash(args):
    if len(args[0].split(" ")) == 1:
        user = args[0].lower()
        c = Cash()
        points = c.get(user)["points"]
        return str(points)
    else:
        user_dict, all_users = get_dict_for_users()
        args = args[0].split(" ")
        action = args[0].lower()
        user = args[1].lower()
        if globals.CURRENT_USER not in user_dict["chatters"]["moderators"]:
            return "This is a moderator-only command"
        try:
            delta = int(args[2])
        except:
            return "The third keyword must be a number"
        c = Cash()
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
