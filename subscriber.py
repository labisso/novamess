import uuid

import logging
logging.basicConfig(level=logging.DEBUG)

import gevent.monkey
gevent.monkey.patch_all()

from novamess import rpc

class HeartbeatSubscriber(object):

    def __init__(self):
        self.topic = uuid.uuid4().hex

    def start(self):
        self.conn = rpc.create_connection(new=True)
        self.conn.create_consumer(self.topic, self, fanout=False)

        # send subscribe request
        ctx = rpc.RpcContext()
        ret = rpc.call(ctx, "heartbeater",
                {"method": "subscribe",
                 "args" : {"subscriber" : self.topic}})

        assert ret is True
        
        #blocking
        self.conn.consume()

    def heartbeat(self, context, beat):
        print "Got heartbeat: %s" % beat

if __name__ == '__main__':
    HeartbeatSubscriber().start()

