from src.lib.queries import Database
import globals


def gift(chan, user, args):
    recipient = args[0].lower().lstrip("@")
    try:
        amount = abs(int(args[1]))
    except:
        return "Amount has to be a number!"
    if recipient == user:
        return "You can't gift yourself cash!"
    channel_info = globals.channel_info[chan]
    if 'gamble' in channel_info and 'time' in channel_info['gamble']:
        if channel_info['gamble']['time'] is not None:
            return "Cheater..."
    db = Database()
    if db.get_user(user, chan):
        if db.get_user(user, chan)[2] >= amount and db.get_user(
                recipient, chan):
            db.modify_points(recipient, chan, amount)
            db.modify_points(user, chan, amount * -1)
            return "{0} cash has been debited to {1}!".format(amount, recipient)
        else:
            return "Those numbers just don't add up. Check your spelling!"
    else:
        return "You don't even have any cash!"
