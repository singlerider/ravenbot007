from src.lib.twitch import get_follower_status


def follower(chan, user, args):
    user = args[0]
    try:
        return get_follower_status(user)
    except:
        return "Something went wrong. RIP."
