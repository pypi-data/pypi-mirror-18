from sulfur.query import Query
from sulfur.queriable import QueriableMixin


class Element(QueriableMixin):
    """
    HTML element of a web page.
    """

    def __init__(self, element, driver):
        self._element = element
        self._driver = driver

    def __getattr__(self, attr):
        return getattr(self._element, attr)

    def fill(self, data):
        """
        Fill input with the given string of data.
        """

        self._element.send_keys(data)

    # Protected methods
    def _get_query_facade_delegate(self):
        return self._element

    def _wrap_element(self, element):
        return Element(element, self._driver)

    def _wrap_query(self, query):
        wrap = self._wrap_element
        return Query(self, [wrap(x) for x in query])
