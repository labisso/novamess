from novamess import rpc
from itertools import count

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import logging
logging.basicConfig(level=logging.DEBUG)

class HeartbeatService(object):

    def __init__(self):
        self.topic = "heartbeater"

        self.subscribers = []
        self.counter = count(0)

    def start(self):
        self.conn = rpc.create_connection(new=True)
        self.conn.create_consumer(self.topic, self, fanout=False)

        gevent.spawn(self._beater)
        
        #blocking
        self.conn.consume()

    def subscribe(self, context, subscriber):
        print "Got subscription: subscriber=%s" % subscriber
        self.subscribers.append(subscriber)
        context.reply(True)

    def _beater(self):
        while True:
            n = self.counter.next()
            logging.debug("Beat %s", n)
            for subscriber in self.subscribers:

                ctx = rpc.RpcContext()

                rpc.cast(ctx, subscriber, {
                    "method": "heartbeat",
                    "args" : {"beat" : n}})

            gevent.sleep(1)

if __name__ == '__main__':
    HeartbeatService().start()

