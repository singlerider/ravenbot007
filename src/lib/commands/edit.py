import src.lib.command_headers as command_headers
import globals


def edit(args):
    command = args[0].lower()
    user_level = args[1]
    response = " ".join(args[2:])
    creator = globals.CURRENT_USER
    if command[0] is "!":
        if command not in command_headers.commands:
            if user_level == "reg" or user_level == "mod":
                return edit_command(command, creator, user_level, response)
                # if "{{}}" in response:
                #    return response.replace("{{}}", globals.CURRENT_USER)
            else:
                return "User level must be 'reg' or 'mod'"
        else:
            return "{} already built in to Lorenzo.".format(command)
    else:
        return "Command must begin with '!'"
