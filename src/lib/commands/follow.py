from src.lib.twitch import get_channel_game


def follow(chan, user, args):
    usage = "!follow [username]"
    if len(args) != 1:
        return usage
    name = args[0].lower().lstrip("@")
    try:
        game = get_channel_game(name)
        return (
            f"THANK YOU {name} for the support!!! Go give their page some "
            f"ravenLove at twitch.tv/{name}, especially if you like {game}!"
        ).format(name, game)
    except Exception:
        return (
            f"THANK YOU {name} for the support!!! Go give their page some "
            f"ravenLove at twitch.tv/{name}!"
        ).format(name)
