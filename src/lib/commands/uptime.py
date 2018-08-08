from src.lib.twitch import *


def uptime(chan, user, args):
    usage = "!uptime"
    uptime = get_stream_uptime(chan)
    if uptime is not None:
        return uptime
    else:
        return "The streamer is offline, duh."
