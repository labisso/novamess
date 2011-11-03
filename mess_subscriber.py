import uuid

import logging
logging.basicConfig(level=logging.DEBUG)

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import mess

class HeartbeatSubscriber(object):

    def __init__(self):
        self.topic = "sub"+uuid.uuid4().hex

    def start(self):
        self.mess = mess.Mess(self.topic, "amqp://guest:guest@127.0.0.1//", "mess")
        self.mess.register_op(self.heartbeat)
        consumer = gevent.spawn(self.mess.consume)

        # send subscribe request
        ret = self.mess.call("messheartbeater", "subscribe", subscriber=self.topic)
        assert ret is True

        consumer.join()

    def heartbeat(self, beat):
        print "Got heartbeat: %s" % beat

if __name__ == '__main__':
    HeartbeatSubscriber().start()

