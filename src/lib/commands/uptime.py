from src.lib.twitch import *
import globals


def uptime():
    usage = "!uptime"
    uptime = get_stream_uptime()
    if uptime is not None:
        return uptime
    else:
        return "The streamer is offline, duh."
