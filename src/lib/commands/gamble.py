from src.lib.gamble import Gamble, initialize
from src.lib.queries import Database
import globals


def gamble(chan, user, args):
    db = Database()
    try:
        points = int(args[0])
    except ValueError:
        return "The points you gamble have to be a number!"
    if points < 10:
        return "The minimum buy-in amount is 10 cash!"
    if points > 10000:
        return "That's too rich for my blood. Try a smaller amount"
    delay = 60
    if db.get_user(user, chan):
        if db.get_user(user, chan)[2] < points:
            return "You don't have enough cash!"
    else:
        return "You've got no cash!"
    g = Gamble(chan)
    if g.check_gamble() is None:
        globals.channel_info[chan]['gamble']["users"][user] = points
        initialize(chan, user, delay, points)
    else:
        return "There is already a gamble in progress!"
