from src.lib.gamble import Gamble, initialize
import globals


def gamble():
    channel = globals.global_channel
    user = globals.CURRENT_USER
    delay = 10
    g = Gamble(channel)
    if g.check_gamble() is None:
        initialize(channel, delay)
    else:
        return "Gambling already in progress!"
