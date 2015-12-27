import time
from threading import Thread


def initialize(irc, crons):
    # start up the cron jobs.
    # config should be in the structure of
    # {
    #   "#channel": [ (period, enabled, callback),.... ]
    #   ...
    # }
    for channel, jobs in crons.items():
        # jobs can be [], False, None...
        if not jobs:
            continue

        for (delay, enabled, callback) in jobs:
            if not enabled:
                continue

            CronJob(irc, channel, delay, callback).start()


class CronJob(Thread):

    def __init__(self, irc, channel, delay, callback):
        Thread.__init__(self)
        self.daemon = True
        self.delay = delay
        self.callback = callback
        self.irc = irc
        self.channel = channel

    def run(self):
        while True:
            time.sleep(self.delay)
            # print(self.callback, self.channel)
            self.irc.send_message(self.channel, self.callback(self.channel))
