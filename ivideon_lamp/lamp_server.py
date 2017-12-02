import asyncio
import struct

class LampServerProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

        message = struct.pack('>cH', bytes([0x12]), 0)
        transport.write(message)

        message = struct.pack('>cH', bytes([0x13]), 0)
        transport.write(message)

        message = struct.pack('>cH3s', bytes([0x20]), 3, bytes([255,255,255]))
        transport.write(message)

        # transport.close()


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(lambda: LampServerProtocol(loop), '127.0.0.1', 9999)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()