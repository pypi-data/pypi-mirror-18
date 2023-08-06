import collections
import functools

import selenium.common.exceptions


def normalize_url(url):
    """
    Forces url to have a correct protocol specification.

    Examples:
        >>> normalize_url('google.com')
        'http://google.com'
    """

    if '://' not in url:
        return 'http://' + url
    return url


def join_url(base_url, url):
    """
    Join two url components.
    """

    return normalize_url(base_url + url)


def wraps_selenium_timeout_error(func):
    """
    Decorator that wraps a function that may emmit a selenium timeout error to
    use Python's native TimeoutError.
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except selenium.common.exceptions.TimeoutException as ex:
            raise TimeoutError(ex)

    return decorated


#
# Special types
#
Shape = collections.namedtuple('Shape', ['width', 'height'])
_Position = collections.namedtuple('Position', ['x', 'y'])


class Position(_Position):
    """
    Represents screen positions.
    """

    def __add__(self, other):
        x, y = other
        return Position(x=self.x + x, y=self.y + y)

    def __sub__(self, other):
        x, y = other
        return self.__add__((-x, -y))
