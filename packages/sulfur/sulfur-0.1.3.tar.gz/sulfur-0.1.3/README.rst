Sulfur is a simplified web driver interface for python-selenium. Sulfur adds
a more pleasant and less java-esque interface and also uses the power of the
BeautifulSoup library to make things easier.

Sulfur's main goal is to facilitate writing tests for Web applications. It has
a builtin pytest plugin that define a few useful fixtures, but it can also be
used with other testing libraries.

You can use Sulfur anywhere that Selenium would be used. Besides the obvious
use case in testing, think of automation, data-mining, presentations, etc.


Basic Usage
===========

Let us start a new webdriver (sulfur uses Chrome by default):

>>> from sulfur import Driver
>>> driver = Driver('chrome', url='http://www.python.org')

The driver object is used to control the web browser. There are several actions
that can be


>>> driver.close()


Selectors and queries
=====================


Page objects
============


Beautiful soup
==============


URL checkers
============


What's up with this name?
=========================

Sulfur is the element that sits just on top of Selenium in the periodic table.
Elements within the same column share many chemical and electronic properties,
but since Sulfur has an atomic number of 16 (against 34 for Selenium), it is
considerably lighter ;)