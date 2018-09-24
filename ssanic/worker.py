import asyncio
import mimetypes
import os
import socket
from datetime import datetime

import uvloop

from ssanic.http.response import Response
from ssanic.parser.request import RequestParser

__all__ = (
    'create_sock_connection',
    'SsanicWorker',
)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def create_sock_connection(host, port, backlog=8):
    # noinspection PyShadowingNames
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(backlog)
    sock.setblocking(False)
    return sock


def _prepare_headers():
    today = datetime.utcnow()
    return [
        ('Date', today.strftime('%a, %d %b %Y %H:%M:%S GMT')),
        ('Server', 'Ssanic'),
        ('Connection', 'close'),
    ]


class SsanicWorker:
    ALLOWED_METHODS = ('GET', 'HEAD')
    INDEX_FILE_NAME = 'index.html'
    SOCK_BUFFER_SIZE = 1024

    def __init__(self, sock, document_root):
        self.document_root = os.path.abspath(document_root)
        self.request_parser = RequestParser()

        self.sock = sock

        self.loop = None

    def idle(self):
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._idle())

    async def _idle(self):
        while True:
            client, _ = await self.loop.sock_accept(self.sock)
            print('REQUEST ACCEPTED {}'.format(client))
            self.loop.create_task(self._handle_request(client))

    async def _handle_request(self, client):
        request = await self._read(client)

        if not self.request_parser(request):
            print('PARSING FAILED {}'.format(client))
            client.close()
            return

        if self.request_parser.request_line.method not in self.ALLOWED_METHODS:
            print('METHOD NOT ALLOWED {}'.format(client))
            response = Response(405, _prepare_headers())
            await self._write(client, response)
            client.close()
            return

        file_path = os.path.abspath(os.path.join(self.document_root, self.request_parser.request_line.path))

        print(self.document_root,
              self.request_parser.request_line.path,
              os.path.join(self.document_root, self.request_parser.request_line.path),
              client)

        if self.document_root not in file_path:
            print('INCORRECT FILE PATH{}'.format(client))
            response = Response(403, _prepare_headers())
            await self._write(client, response)
            client.close()
            return

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, self.request_parser.request_line.INDEX_FILE_NAME)

        if not os.path.exists(file_path):
            print('{} File not exist'.format(client))
            response = Response(404, _prepare_headers())
            await self._write(client, response)
        else:
            print('{} OK'.format(client))

            headers = _prepare_headers()
            headers.append(('Content-Length', str(os.path.getsize(file_path))))
            mime_type, _ = mimetypes.guess_type(file_path)
            headers.append(('Content-Type', mime_type))

            response = Response(200, headers)

            with open(file_path, 'rb') as fp:
                await self._write(client, response, fp)

        client.close()

    async def _read(self, client):
        return (await self.loop.sock_recv(client, self.SOCK_BUFFER_SIZE)).decode('utf-8')

    async def _write(self, client, response, fp=None):
        await self.loop.sock_sendall(client, str(response).encode('utf-8'))

        if fp is not None:
            while True:
                line = fp.read(self.SOCK_BUFFER_SIZE)

                if not line:
                    return

                await self.loop.sock_sendall(client, line)


if __name__ == '__main__':
    sock = create_sock_connection('localhost', 8001)
    worker = SsanicWorker(sock, '/tmp')

    try:
        worker.idle()
    except KeyboardInterrupt:
        sock.close()
