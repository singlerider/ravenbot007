from src.lib.gamble import Gamble
from src.lib.queries import Database
import globals


def join():
    channel = globals.CURRENT_CHANNEL
    user = globals.CURRENT_USER
    db = Database()
    g = Gamble(channel)
    if g.check_gamble() is not None:
        points = globals.channel_info[globals.CURRENT_CHANNEL][
            'gamble']["points"]
        if db.get_user(user, channel):
            if db.get_user(user, channel)[2] < points:
                return "You don't have enough cash!"
        else:
            return "You've got no cash!"
        globals.channel_info[globals.CURRENT_CHANNEL]['gamble'][
            "users"][user] = True
        return "{0} has joined the action and is on the hook for {1} cash!".format(
            user, points)
    else:
        return "There's no gamble to join. Start one with '!gamble [amount]'!"
