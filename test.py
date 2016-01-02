#!/usr/bin/env python2.7
import globals
from src.lib.queries import Database
from src.lib.gamble import Gamble

if __name__ == "__main__":
    n = 0
    while n < 11:
        globals.channel_info = {"testchannel": {"gamble": {
            "time": None, "users": {}}}}
        g = Gamble()
        print g.check_gamble()
        g.initiate_gamble()
        print g.check_gamble()
        g.terminate_gamble()
        print g.check_gamble()
        print g.rob_yield()
        n += 1
