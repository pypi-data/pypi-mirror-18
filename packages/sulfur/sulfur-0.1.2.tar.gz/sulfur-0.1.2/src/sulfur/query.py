from collections import Sequence


class Query(Sequence):
    """
    A query of elements in a page.

    Queries can be filtered and iterated. Most query methods can be chained
    as in the example:

    >>> q = ...  # driver method that return a query object
    >>> q.filter('div').click()                                  # pytest: +SKIP
    """

    def __init__(self, parent, elements):
        self.parent = parent
        self.elements = elements

    def click(self):
        """
        Clicks on all selected elements.
        """

        [x.click() for x in self]
        return self

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, i):
        return self.elements[i]