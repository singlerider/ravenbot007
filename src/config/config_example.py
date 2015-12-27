global config

channels_to_join = ['#acarlton5']

for channel in channels_to_join:
    channel = channel.lstrip('#')

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'Pikachu__bot',
    # get this from http://twitchapps.com/tmi/
    'oauth_password': 'oauth:6yc3lsd1ho0jmw52vr58udcy2mqe32',

    'debug': True,
    'log_messages': True,

    'channels': channels_to_join,
}
