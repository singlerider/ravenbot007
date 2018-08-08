from src.lib.queries import Database
import src.lib.command_headers as command_headers


def rem(chan, user, args):
    db = Database()
    command = args[0].lower()
    command_data = db.get_command(command, chan)
    if command_data:
        db.remove_command(command, chan)
        return "{0} removed from Ravenbot007's custom commands!".format(
            command)
    else:
        return "{0} not found.".format(command)
