from src.lib.queries import Database
import globals


def top10():
    db = Database()
    channel = globals.global_channel
    rank_data = db.get_top10(channel)
    # [(1, u'singlerider', 441, u'ravenbot007'), (2, u'nano_machina', 129, u'ravenbot007')]
    candidates = ", ".join([x[1] + ": " + str(x[2]) for x in rank_data])
    resp = "The top 10 cash holders are... " + candidates
    return resp
