import src.lib.command_headers as headers


def commands(chan, user, args):
    return str(", ".join(sorted(headers.commands))).replace("!", "")
