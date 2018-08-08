from src.lib.queries import Database


def remquote(chan, user, args):
    db = Database()
    try:
        _id = int(args[0])
    except:
        return "The quote id must be a number"
    db.remove_quote(chan, _id)
    # will give a success message no matter if the id exists or not
    return "Quote #{0} removed!".format(_id)
