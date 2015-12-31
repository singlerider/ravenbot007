from src.lib.twitch import *
import globals


def uptime():
    usage = "!uptime"
    uptime = get_stream_uptime()
    channel = globals.global_channel
    if get_stream_status():
        return "The current !uptime is " + str(uptime)
    else:
        return globals.global_channel + " is offline."
