import globals


def pot(chan, user, args):
    current_pot = 0
    try:
        if globals.channel_info[chan]['gamble']["time"] is not None:
            gamble = globals.channel_info[chan]['gamble']
            current_pot = len(gamble["users"]) * gamble["points"]
        else:
            return "There is no gamble, currently!"
    except Exception as error:
        print(error)
        return "There is no gamble, currently!"
    return "The current pot is {0}! '!join' in!".format(current_pot)
