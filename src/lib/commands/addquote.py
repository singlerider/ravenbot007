from src.lib.queries import Database
from src.lib.twitch import get_stream_game
import globals

def addquote(args):
    db = Database()
    user = globals.CURRENT_USER
    channel = globals.global_channel
    quote = unicode(args[0].strip().strip("\"").strip("\'"), 'utf-8')
    game = get_stream_game(channel)
    db.add_quote(channel, user, quote, game)
    return "{0} added!".format(quote)
