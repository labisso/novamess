from itertools import count

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import logging
logging.basicConfig(level=logging.DEBUG)

import mess

class HeartbeatService(object):

    def __init__(self):
        self.topic = "messheartbeater"

        self.subscribers = []
        self.counter = count(0)

    def start(self):
        self.mess = mess.Mess(self.topic, "amqp://guest:guest@127.0.0.1//", "mess")
        self.mess.register_op(self.subscribe)

        gevent.spawn(self.mess.consume)
        gevent.spawn(self._beater).join()

    def subscribe(self, subscriber):
        print "Got subscription: subscriber=%s" % subscriber
        self.subscribers.append(subscriber)
        return True

    def _beater(self):
        while True:
            n = self.counter.next()
            logging.debug("Beat %s", n)
            for subscriber in self.subscribers:

                self.mess.fire(subscriber, "heartbeat", beat=n)

            gevent.sleep(1)

if __name__ == '__main__':
    HeartbeatService().start()

