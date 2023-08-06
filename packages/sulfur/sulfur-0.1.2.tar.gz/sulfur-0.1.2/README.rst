Sulfur is a simplified web driver interface for python-selenium. Sulfur adds
a more pleasant and less java-esque interface and also uses the power of the
BeautifulSoup library to make things easier.

Sulfur's main goal is to be used for writing tests for Web applications. It has
a builtin pytest plugin that define a few useful fixtures.

Of course, you can use Sulfur anywhere that Selenium would be used: think of
automation, data-mining, etc.


Basic Usage
===========

Let us start a new webdriver (sulfur uses Chrome by default):

>>> from sulfur import Driver

>>> driver = Driver()

The sulfur driver exposes the selenium API, but add a few candies:

>>> driver.open('http://www.python.org')

For instance, .get_element_by_id() can be replaced by a simple query using the
getitem interface:

#    >>> driver.ui['#id-search-field'] == driver.find_element_by_id('id-search-field')
#    True


Don't forget to close driver (and consequentially, the browser) after use

>>> driver.close()

What's up with this name?
=========================

Sulfur is the element that sits just on top of Selenium in the periodic table.
Elements within the same column share many chemical and electronic properties,
but since Sulfur has an atomic number of 16 (against 34 for Selenium), it is
considerably lighter ;)