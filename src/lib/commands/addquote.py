from src.lib.queries import Database
from src.lib.twitch import get_stream_game
import globals


def addquote(args):
    db = Database()
    user = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    quote = str(args[0].strip().strip("\"").strip("\'"), 'utf-8')
    stripped_quote = str("".join(i for i in quote if ord(i) < 128))
    if len(quote) > 300:
        return "Let's keep it below 300 characters?"
    game = get_stream_game(channel)
    db.add_quote(channel, user, quote, game)
    most_recent_quote_id = db.get_most_recent_quote_id(channel)[0]
    return "#{0}: {1} added!".format(most_recent_quote_id, stripped_quote)
