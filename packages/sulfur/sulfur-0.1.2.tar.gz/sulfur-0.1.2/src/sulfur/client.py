import requests
from lazyutils import delegate_to, lazy


class Client:
    """
    Abstract HTTP client.
    """

    DEFAULT_CONCRETE_CLASS = None

    def __new__(cls, **kwargs):
        cls = get_client_class()
        new = object.__new__(cls)
        new.__init__(**kwargs)
        return new

    def __init__(self, base_url=None):
        self.base_url = base_url

    def url_normalize(self, url):
        return (self.base_url or '') + url

    def get(self, url, data=None):
        """
        Opens url using GET.

        Return a Page() instance.
        """

        raise NotImplementedError

    def post(self, url, data=None):
        """
        Opens url using POST.

        Return a Response() instance.
        """

        raise NotImplementedError


class Response:
    """
    Base class for all responses.

    Attributes:
        content (bytes):
            A raw byte-string with the response data.
        data (str):
            Content as a decoded string.
        status_code:
            Numeric HTTP status code (e.g., 200, 404, etc)
        encoding (str):
            Data encoding
        url (str):
            Request absolute URL
        header (dict):
            A dictionary-like object with the HTTP headers.
    """

    @lazy
    def data(self):
        return self.content.decode(self.encoding)

    content = delegate_to('_data')
    status_code = delegate_to('_data')
    encoding = delegate_to('_data')
    url = delegate_to('_data')
    header = delegate_to('_data')


class HttpResponse(Response):
    """
    Represents a response to an HTTP request.
    """

    def __init__(self, data):
        self._data = data


class HttpClient(Client):
    """
    Client that performs actual HTTP requests
    """

    def get(self, url, data=None):
        url = self.url_normalize(url)
        response = requests.get(url, data)
        return HttpResponse(response)


class DjangoClient(Client):
    """
    Django-based client interface.
    """


def get_client_class():
    """
    Return the default global client class.
    """

    if Client.DEFAULT_CONCRETE_CLASS is None:
        return HttpClient
    else:
        return Client.DEFAULT_CONCRETE_CLASS


def set_client_class(cls):
    """
    Sets the global default client class.
    """

    Client.DEFAULT_CONCRETE_CLASS = cls
