from src.lib.gamble import Gamble
from src.lib.queries import Database
import globals


def join(chan, user, args):
    db = Database()
    g = Gamble(chan)
    if g.check_gamble() is not None:
        user_is_already_gambling = g.get_gamble_user(user)
        if user_is_already_gambling:
            return "You're already gambling. Perhaps you need a 12 step program?"
        points = globals.channel_info[chan][
            'gamble']["points"]
        if db.get_user(user, chan):
            if db.get_user(user, chan)[2] < points:
                return "You don't have enough cash!"
        else:
            return "You've got no cash!"
        globals.channel_info[chan]['gamble'][
            "users"][user] = True
        return "{0} has joined the action and is on the hook for {1} cash!".format(
            user, points)
    else:
        return "There's no gamble to join. Start one with '!gamble [amount]'!"
