from src.lib.gamble import Gamble, initialize
from src.lib.queries import Database
import globals


def gamble(args):
    db = Database()
    try:
        points = int(args[0])
    except:
        return "The points you gamble have to be a number!"
    channel = globals.global_channel
    user = globals.CURRENT_USER
    delay = 60
    if db.get_user(user, channel):
        if db.get_user(user, channel)[2] < points:
            return "You've only got {0} cash!".format(db.get_user(user)[2])
    else:
        return "You've got no cash!"
    g = Gamble(channel)
    if g.check_gamble() is None:
        globals.channel_info[channel]['gamble']["users"][
            user] = points
        initialize(channel, user, delay, points)
    else:
        globals.channel_info[channel]['gamble']["users"][
            user] = points
