import os
import sys
from subprocess import Popen
from http import server
import threading


class TestServer:
    """
    Starts http.server simple server.
    """

    def __init__(self, port=8000, path=None, force_subprocess=False):
        path = path or os.getcwd()
        self.port = port
        self.path = path
        self._target = None
        self._subprocess = force_subprocess

    def start(self):
        """
        Starts serving.
        """

        if self._subprocess:
            command = [sys.executable, '-m', 'http.server', str(self.port)]
            self._process = Popen(command, cwd=self.path)
        else:
            self._target = threading.Thread(target=self._serve, daemon=True)
            self._target.start()

    def stop(self):
        """
        Stops server.
        """

        if self._target is not None and self._subprocess:
            self._target.terminate()
        elif self._target is not None:
            self._srv.server_close()
            self._target.join(timeout=0)
        else:
            raise RuntimeError('server not initialized.')
        self._target = None

    def _serve(self):
        class HTTPHandler(BaseHTTPHandler):
            cwd = self.path

        addr = ('', self.port)
        self._srv = server.HTTPServer(addr, HTTPHandler)
        self._srv.serve_forever()


class BaseHTTPHandler(server.SimpleHTTPRequestHandler):
    local_cwd = os.getcwd()

    @property
    def cwd(self):
        raise NotImplementedError

    def translate_path(self, path):
        new_path = super().translate_path(path)

        if new_path.startswith(self.local_cwd):
            new_path = new_path[len(self.local_cwd) + 1:]
            new_path = os.path.join(self.cwd, new_path)
        return new_path
