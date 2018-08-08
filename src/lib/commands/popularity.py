from src.lib.twitch import *


def popularity(chan, user, args):

    game = args[0]

    return get_game_popularity(game)
