import asyncio

from ivideon_lamp.management import get_commands

HOST = '127.0.0.1'
PORT = 9999

TYPE_SIZE = 1
LENGTH_SIZE = 2
HEADER_LENGTH = TYPE_SIZE + LENGTH_SIZE


def do_command(type, value=None):
    for cls in get_commands():
        if cls.type == type:
            print('New command from server')
            cmd = cls(value)
            cmd.run()


class Client:
    # modes
    parse_header = 1
    parse_value = 2

    def __init__(self, loop, host, port, timeout=1, max_attempts=5):
        self.loop = loop
        self.host = host
        self.port = port
        self._reader = None
        self._writer = None
        self._attemps = 0
        self.timeout = timeout
        self.max_attempts = max_attempts

    @asyncio.coroutine
    def open_connection(self, is_reconnect=False):
        self._reader = None
        self._writer = None

        if is_reconnect:
            while (self.max_attempts == 0 or self._attemps < self.max_attempts):
                self._attemps += 1

                print('Trying to reconnect to %s:%s' % (self.host, self.port))
                yield from asyncio.sleep(self.timeout)

                try:
                    self._reader, self._writer = yield from asyncio.open_connection(
                        self.host, self.port, loop=self.loop)
                except ConnectionRefusedError:
                    pass
                else:
                    print('Connected to %s:%s' % (self.host, self.port))
                    break
        else:
            # Don't catch exceptions for first connection,
            # let's show it on console.
            self._reader, self._writer = yield from asyncio.open_connection(
                self.host, self.port, loop=self.loop)
            print('Connected to %s:%s' % (self.host, self.port))

    @asyncio.coroutine
    def parse(self):
        """Parse the body.
        Stops work only if the EOF was received."""
        buffer = b''
        parse_value = False
        type = None
        length = None
        value = None
        mode = self.parse_header

        while not self._reader.at_eof():
            if mode == self.parse_header:
                buffer += yield from self._reader.read(HEADER_LENGTH)
                if len(buffer) < HEADER_LENGTH:
                    continue

                data = buffer[:HEADER_LENGTH]
                type, length = data[0], data[1:]
                buffer = buffer[HEADER_LENGTH:]
                
                length = int.from_bytes(length, 'big')
                if length:
                    mode = self.parse_value
                else:
                    do_command(type)
                    type = None
                    length = None
            elif mode == self.parse_value:
                buffer += yield from self._reader.read(length)
                if len(buffer) < length:
                    continue

                value = buffer[:length]
                buffer = buffer[length:]

                value = int.from_bytes(value, 'big')
                do_command(type, value)
        
                type = None
                length = None
                value = None
                mode = self.parse_header
            else:
                break

    def close(self):
        if self._writer is not None:
            self._writer.close()

    @asyncio.coroutine
    def run(self):
        yield from self.open_connection()
        while (self._reader is not None and self._writer is not None):
            yield from self.parse()
            yield from self.open_connection(True)


def main():
    host = input('Enter server address (default %s): ' % HOST) or HOST
    port = input('Enter tcp port number (default %s): ' % PORT) or PORT

    loop = asyncio.get_event_loop()
    client = Client(loop, host, port)
    try:
        loop.run_until_complete(client.run())
    except KeyboardInterrupt:
        client.close()
    loop.close()


if __name__ == '__main__':
    main()