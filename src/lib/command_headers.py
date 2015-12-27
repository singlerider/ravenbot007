commands = {

    '!commands': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!commands'
    },

    '!followers': {
        'limit': 30,
        'return': 'command',
        'argc': 0,
        'usage': '!followers'

    },

    '!follower': {
        'limit': 0,
        'return': 'command',
        'argc': 1,
        'usage': '!follower [username]',
        #'ul': 'mod'

    },

    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime'

    },

    '!stream': {
        'limit': 60,
        'return': 'command',
        'argc': 0,
        'usage': '!stream'

    },

    '!popularity': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        #'ul': 'mod',
        'usage': '!popularity [name_of_game]'
    },

    '!follow': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!follow [streamer_username]',
        #'ul': 'mod'

    },

    '!donation': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!donation [username] [dollar_amount]',
        #'ul': 'mod'
    }
}


def initalizeCommands(config):
    for channel in config['channels']:
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
