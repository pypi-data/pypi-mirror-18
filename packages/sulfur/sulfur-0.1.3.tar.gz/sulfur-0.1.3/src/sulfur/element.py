from sulfur.queriable import QueriableMixin
from sulfur.query import Query
from sulfur.utils import Position, Shape


class Element(QueriableMixin):
    """
    HTML element of a web page.
    """

    @property
    def id(self):
        return self._element.id

    @property
    def is_displayed(self):
        return self._element.is_displayed

    @property
    def is_enabled(self):
        return self._element.is_enabled

    @property
    def is_selected(self):
        return self._element.is_selected

    @property
    def position(self):
        """
        Element's position.
        """

        pos = self._element.location
        return Position(**pos)

    @property
    def shape(self):
        """
        Element's shape.
        """

        shape = self._element.size
        return Shape(**shape)

    @property
    def text(self):
        """
        Text content for element. Strips HTML tags.
        """

        return self._element.text

    @property
    def type(self):
        """
        Return the HTML tag name for element.
        """

        return self._element.tag_name

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

    def clear(self):
        """
        Clear any input text present in element.
        """

        self._element.clear()

    def attr(self, name, *args):
        """
        Return an element's attribute.

        If called with two arguments, sets the attribute value.
        """

        if not args:
            return self._element.get_attribute(name)

        value, = args
        raise NotImplementedError

    def property(self, name, *args):
        """
        Return an element's property.

        If called with two arguments, sets the property value.
        """

        if not args:
            return self._element.get_property(name)

        value, = args
        raise NotImplementedError

    def css(self, name):
        """
        Return value of CSS property.
        """

        return self._element.value_of_css_property(name)

    # Protected methods
    def _get_query_facade_delegate(self):
        return self._element

    def _wrap_element(self, element):
        return Element(element, self._driver)

    def _wrap_query(self, query):
        wrap = self._wrap_element
        return Query(self, [wrap(x) for x in query])
