What?
=====

Experimental use of (modified) RPC code from OpenStack Nova as a standalone
messaging library. Initial code from nova was copied from::

    830760b4c79cf9cdc80c6e0047ea206abc21f2c6
    Wed Nov 2 15:44:31 2011 +0000

Files::

    nova/rpc/impl_kombu.py


Example Usage
=============

There is a simple service that sends out heartbeats to subscribers.

1. Make a virtualenv and activate it

2. Install dependencies::

   $ pip install kombu gevent

3. Run the heartbeater service::

   $ python heartbeater.py

4. In another terminal, start the subscriber::

   $ python subscriber.py


