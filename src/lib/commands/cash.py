from src.lib.twitch import *
from src.lib.queries import Database


class Cash:
    def add_all(channel, points):
        user_dict, all_users = get_dict_for_users(channel)
        db = Database()
        db.add_user(all_users)
        for user in all_users:
            db.modify_points(user, points)
        print "added points to {0}".format(users)
        return {"users": all_users, "points": points}

    def add(users, points):
        db = Database()
        db.add_user(users)
        modify_points(users[0], points)
        print "added {0} points to {1}".format(points)
        return {"user": users[0], "points": points}

    def modify(users, points):
        db = Database()
        db.add_user(users)
        modify_points(users[0], points)
        print "modified {0}'s points by {1}".format(users[0], points)
        return {"user": users[0], "points": points}

    def get(user):
        db = Database()
        if len > 0:
            user_points = db.get_user(user)[0]  # (3, u'testuser', 5, u'mod')
            return {"user": user, "points": points}
        else:
            return {}


def cron(channel):
    c = Cash()
    points_added_to = c.add_all(channel, 1)
    print "performed points cron"


def cash(args):
    if len(args.split(" ")) == 1:
        # TODO add points check
        pass
    else:
        args = args.aplit(" ")
        action = args[0].lower()
        user = args[1].lower()
        try:
            delta = int(args[2])
        except:
            return "The third keyword must be a number"
        c = Cash()

        if action == "add" or action == "remove" or action == "set":
            if action == "add":
                if user == "all":
                    user_dict, all_users = get_dict_for_users()
                    c.modify(all_users)
                else:
                    c.modify([user], abs(delta))
            elif action == "remove":
                c.remove([user], abs(delta) * -1)
            elif action == "set":
                return "This one is still in progress"
        else:
            return "The first keyword must be either 'add', 'remove', or 'set'"
