from src.lib.twitch import *
from src.lib.channel_data import ChannelData
import globals

def hosts():
    cd = ChannelData(globals.global_channel)
    channel_id = cd.get_channel_id_from_db()[0]
    print channel_id
    hosts = get_hosts(channel_id)
    return "You've got " + str(len(hosts)) + " people hosting you!"
