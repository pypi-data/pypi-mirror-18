# from .. import BaseHandler
from utils import *

import asyncio


class HttpHandler(asyncio.Protocol):
    """
    Copied twisted.protocols.telnet.Telnet mechanism.
    """

    def __init__(self, honeypot):
        self.honeypot = honeypot

    def connection_made(self, transport):
        self.honeypot.active_attacks += 1
        self.transport = transport
        print("Connection from {0}".format(self.transport.get_extra_info('peername')[0]))

    def data_received(self, data):
        self.prepare_save(data)
        self.transport.write(b"asdqweqwe")
        self.transport.close()

    def prepare_save(self, data):
        attack_time = time.time()
        json_data = {
            'from':self.transport.get_extra_info('peername')[0],
            'protocol':'http',
            'time':attack_time,
            'request_header':data
        }
        self.save_data(json_data)

    def connection_lost(self, exc):
        print("Connection lost from {0}".format(self.transport.get_extra_info('peername')[0]))
        self.honeypot.active_attacks -= 1


class HttpHoneypot:

    syslog = False
    sqlite = False
    agents = []

    active_attacks = 0

    interfaces = ['0.0.0.0']
    port = 23

    handler = HttpHandler


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    hp = HttpHoneypot()

    coro = loop.create_server(lambda: hp.handler(hp), '0.0.0.0', 80)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        hp.stop()
        print("\nServer Closed")

    loop.close()