from src.lib.queries import Database
from src.lib.twitch import get_dict_for_users

TEST_USER = "singlerider"


class Cash:
    def __init__(self, channel):
        self.db = Database()
        self.channel = channel

    def add_all(self, points):
        user_dict, all_users = get_dict_for_users(self.channel)
        self.db.add_user(all_users, self.channel)
        for user in all_users:
            self.db.modify_points(user, self.channel, points)
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

    def rank(self, user):
        user_data = self.db.get_cash_rank(user, self.channel)
        if user_data:
            return {
                "user": user_data[0], "channel": self.channel,
                "points": user_data[1], "rank": user_data[3]
                }
        else:
            return {
                "user": user, "channel": self.channel, "points": 0,
                "rank": None
                }


def cron(channel):
    c = Cash(channel)
    c.add_all(channel, 1)
    print("performed points cron")


def cash(chan, user, args):
    c = Cash(chan)
    if args:
        args = args[0].split(" ")
    if len(args) < 1:
        points = c.get(user)["points"]
        return str(points)
    elif len(args) == 1:
        user = args[0].lower().lstrip("@")
        rank_data = c.rank(user)
        if rank_data["rank"] is not None:
            points = rank_data["points"]
            rank = rank_data["rank"]
            return f"{points} cash, which makes you number {rank}!"
        else:
            return "User not found"
    else:
        action = args[0].lower()
        user_to_give = args[1].lower()
        if user != chan and user != TEST_USER:
            return f"Only {chan} can do that."
        try:
            delta = int(args[2])
        except ValueError:
            return "The third keyword must be a number"
        if action == "add" or action == "remove" or action == "set":
            if action == "add":
                if user_to_give == "all":
                    cash_response = c.add_all(delta)
                    return "Added {0} cash to {1} Conspirators".format(
                        delta, len(cash_response["users"]))
                else:
                    c.modify([user_to_give], abs(delta))
                    return "Added {0} cash to {1}".format(delta, user_to_give)
            elif action == "remove":
                c.modify([user_to_give], abs(delta) * -1)
                return "Removed {0} cash from {1}".format(delta, user_to_give)
            elif action == "set":
                return "This one is still in progress"
        else:
            return "The first keyword must be either 'add', 'remove', or 'set'"
