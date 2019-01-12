from src.lib.queries import Database

TEST_USER = "singlerider"


def get_user_luck(chan, user):
    db = Database()
    gamble_entries = []
    wins = 0
    gamble_entries = db.get_gamble_user_entries(user=user, channel=chan)
    for gamble_entry in gamble_entries:
        if gamble_entry[5]:
            wins += 1
    try:
        win_ratio = (wins / len(gamble_entries)) * 100
    except ZeroDivisionError:
        win_ratio = 0.0
    return (win_ratio, wins, len(gamble_entries))


def luck(chan, user, args):
    win_ratio = (0.0, 0, 0)
    if not args:
        win_ratio = get_user_luck(chan, user)
        return (
            f"{user}'s win ratio is {win_ratio[0]:.3f}% "
            f"({win_ratio[1]} wins out of {win_ratio[2]})"
        )
    elif user == chan or user == TEST_USER:
        win_ratio = get_user_luck(chan, args[0].lower())
        return (
            f"{args[0]}'s win ratio is {win_ratio[0]:.3f}% "
            f"({win_ratio[1]} wins out of {win_ratio[2]})"
        )
    else:
        return f"Only {chan} can do that!"
