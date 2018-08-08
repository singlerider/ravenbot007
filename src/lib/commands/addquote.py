from src.lib.queries import Database
from src.lib.twitch import get_stream_game


def addquote(chan, user, args):
    db = Database()
    quote = args[0].strip().strip("\"").strip("\'")
    stripped_quote = str("".join(i for i in quote if ord(i) < 128))
    if len(quote) > 300:
        return "Let's keep it below 300 characters?"
    game = get_stream_game(chan)
    db.add_quote(chan, user, quote, game)
    most_recent_quote_id = db.get_most_recent_quote_id(chan)[0]
    return "#{0}: {1} added!".format(most_recent_quote_id, stripped_quote)
