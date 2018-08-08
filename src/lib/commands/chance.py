from src.lib.queries import Database
from src.lib.gamble import Gamble


def chance(chan, user, args):
    db = Database()
    g = Gamble(chan)
    points = abs(g.rob_yield(multiplier=1))
    db.add_user([user], chan)
    db.modify_points(user, chan, points)
    print((user, points, chan))
    if points ==  0:
        resp = "Nothing this time! Try again in a half hour?"
    else:
        resp = "You got {0} cash!".format(points)
    return resp
