from src.lib.queries import Database
import src.lib.command_headers as command_headers
import globals


def rem(args):
    db = Database()
    command = args[0].lower()
    db.remove_command(command)
    return "{0} removed from Ravenbot007's custom commands!".format(
        command)
