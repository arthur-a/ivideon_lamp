import binascii
import asyncio
import struct

from ivideon_lamp.management import get_commands

HOST = '127.0.0.1'
PORT = 9999

TYPE_SIZE = 1
LENGTH_SIZE = 2
MIN_LENGTH = TYPE_SIZE + LENGTH_SIZE

MAX_ATTEMPTS = 3


def do_command(type, value=None):
    for cls in get_commands():
        if cls.type == type:
            print('New command from server')
            cmd = cls(value)
            cmd.run() 


@asyncio.coroutine
def handle_reader(reader):
    buffer = b''
    parse_value = False
    type = None
    length = None
    value = None

    while True:
        buffer += yield from reader.read(100)

        while True:
            if not parse_value and len(buffer) >= MIN_LENGTH:
                data = buffer[:MIN_LENGTH]
                buffer = buffer[MIN_LENGTH:]
                
                try:
                    type, length = struct.unpack('>cH', data)
                except (struct.error, TypeError):
                    continue

                type = int(binascii.hexlify(type), 16)
                
                if length:
                    parse_value = True
                else:
                    do_command(type)
                    type = None
                    length = None
            elif parse_value and len(buffer) >= length:
                parse_value = False
                data = buffer[:length]
                buffer = buffer[length:]

                try:
                    value = struct.unpack('>%is' % length, data)[0]
                except (struct.error, TypeError):
                    value = b''

                if value != b'':
                    value = int(binascii.hexlify(value), 16)            
                    do_command(type, value)
        
                type = None
                length = None
                value = None
            else:
                break

        if reader.at_eof():
            break


def main(host, port):
    loop = asyncio.get_event_loop()

    reader, writer = loop.run_until_complete(asyncio.open_connection(
        host, port, loop=loop))
    print('Connected to %s:%s' % (host, port))

    attemps = 0
    while True:
        try:
            loop.run_until_complete(handle_reader(reader))
        except KeyboardInterrupt:
            writer.close()
            break

        loop.run_until_complete(asyncio.sleep(2))

        print('Trying to reconnect to %s:%s' % (host, port))
        attemps += 1
        try:
            reader, writer = loop.run_until_complete(asyncio.open_connection(
                host, port, loop=loop))
        except ConnectionRefusedError:
            pass

        if attemps == MAX_ATTEMPTS:
            break
    
    loop.close()


if __name__ == '__main__':
    host = input('Enter server address (default %s): ' % HOST) or HOST
    port = input('Enter tcp port number (default %s): ' % PORT) or PORT
    main(host, port)
