from src.lib.queries import Database
import globals


def remquote(args):
    db = Database()
    channel = globals.CURRENT_CHANNEL
    try:
        _id = int(args[0])
    except:
        return "The quote id must be a number"
    db.remove_quote(channel, _id)
    # will give a success message no matter if the id exists or not
    return "Quote #{0} removed!".format(_id)
