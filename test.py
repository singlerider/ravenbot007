#!/usr/bin/env python2.7

from src.lib.queries import Database
from src.lib.gamble import Gamble

if __name__ == "__main__":
    g = Gamble()
    print g.check_gamble()
    g.initiate_gamble()
    print g.check_gamble()
    g.terminate_gamble()
    print g.check_gamble()
    print g.rob_yield()
