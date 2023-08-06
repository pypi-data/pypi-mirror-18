import os
import threading
from http import server


class TestServer:
    """
    Runner for http.server simple server.
    """

    @property
    def base_url(self):
        return 'http://localhost:%s/' % self.port

    @property
    def running(self):
        return self._target is not None

    def __init__(self, port=8000, path=None, poll_interval=0.5):
        path = path or os.getcwd()
        self.port = port
        self.path = path
        self._target = None
        self._server_obj = None
        self.poll_interval = poll_interval

    def start(self):
        """
        Starts serving.
        """

        class HTTPHandler(BaseHTTPHandler):
            cwd = self.path

        addr = ('', self.port)
        self._server_obj = server.HTTPServer(addr, HTTPHandler)
        target = self._server_obj.serve_forever
        self._target = threading.Thread(target=target,
                                        daemon=True,
                                        args=(self.poll_interval,))
        self._target.start()

    def stop(self):
        """
        Stops server.
        """

        if self._target is not None:
            self._server_obj.shutdown()
            self._target.join(timeout=self.poll_interval)
            self._server_obj.server_close()
        else:
            raise RuntimeError('server not initialized.')
        self._target = None


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
