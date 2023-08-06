from bs4 import BeautifulSoup
from lazyutils import lazy, delegate_to
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sulfur.element import Element
from sulfur.id_manager import IdManager
from sulfur.query import Query
from sulfur.queriable import QueriableMixin
from sulfur.utils import normalize_url


class DriverBase(QueriableMixin):
    """
    A simplified interface to the selenium webdriver with simpler method names
    and a few useful resources.
    """

    _soup_lib = 'html5lib'

    title = delegate_to('_driver')

    @property
    def selenium(self):
        """
        Selenium web driver object.
        """

        return self._driver

    @lazy
    def soup(self):
        """
        A beautiful soup interface to the HTML source code
        """

        return BeautifulSoup(self.page, self._soup_lib)

    @property
    def page(self):
        """
        Current page object.
        """

        return self._page

    @property
    def id(self):
        """
        A simplified interface to dom elements with a defined id.
        """

        return IdManager(self)

    def __init__(self, driver, url='', wait=0):
        self._driver = driver
        self._page = None
        self.base_url = url and normalize_url(url)
        self._driver.implicitly_wait(wait)

    def __call__(self, selector):
        elements = self._driver.find_elements_by_css_selector(selector)
        return Query(self, [self._wrap_element(x) for x in elements])

    def __getitem__(self, selector):
        elem = self._driver.find_element_by_css_selector(selector)
        return self._wrap_element(elem)

    def open(self, url=''):
        """
        Opens the given url.

        Returns a page object.
        """

        self.url = normalize_url(self.base_url + url)
        return self._driver.get(self.url)

    def click(self, selector):
        """
        Clicks in the first element with the given CSS selector.
        """

        self[selector].click()

    def close(self, quit=True):
        """
        Closes the current web browser tab.

        If quit=True, forces the browser to quit even if there are other tabs
        open. Most browsers will quit when there are no tabs left.
        """

        if quit:
            self._driver.quit()
        else:
            self._driver.close()

    def send(self, *args):
        """
        Alias to send_keys().
        """

        return self._driver.send_keys(*args)

    def restart(self):
        """
        Restart the web driver and go to the current url.
        """

        self._driver = type(self._driver)()
        self.open(self.url)

    # Wait conditions
    def wait_on(self, func, timeout=1.0):
        """
        Wait until func(driver) return True.

        Raises a TimeoutError if condition is not met in the given timeout
        interval.
        """

        WebDriverWait(self, timeout).until(func)

    def wait_title(self, value, timeout=1.0):
        """
        Waits until the page title assumes the given value.

        Raises a TimeoutError if condition is not met in the given interval.
        """

        condition = EC.title_is(value)
        WebDriverWait(self, timeout).until(condition)

    def wait_title_contains(self, value, timeout=1.0):
        """
        Waits until the page title contains the given value.

        Raises a TimeoutError if condition is not met in the given interval.
        """

        condition = EC.title_contains(value)
        WebDriverWait(self, timeout).until(condition)

    # Private methods
    def _wrap_element(self, element):
        return Element(element, self)

    def _wrap_query(self, query):
        wrap = self._wrap_element
        return Query(self, [wrap(x) for x in self])

    def _get_query_facade_delegate(self):
        return self._driver


class Driver(DriverBase):
    """
    The sulfur web driver.

    Args:
        driver:
            If given, can be a string or a Selenium webdriver object. Strings
            must be on the list: "firefox", "chromium".
            Of course you should have the corresponding web browser installed
            in your system.
    """

    def __init__(self, driver=None, **kwargs):
        if driver is None:
            driver = 'phantomjs'
        if isinstance(driver, str):
            driver_cls = get_driver_class_from_string(driver)
            driver = driver_cls()
        super().__init__(driver=driver, **kwargs)


def get_driver_class_from_string(name):
    """
    Select driver class from name.
    """

    mapping = {
        'firefox': 'selenium.webdriver.Firefox',
        'chrome': 'selenium.webdriver.Chrome',
        'ie': 'selenium.webdriver.Ie',
        'edge': 'selenium.webdriver.Edge',
        'opera': 'selenium.webdriver.Opera',
        'safari': 'selenium.webdriver.Safari',
        'blackberry': 'selenium.webdriver.BlackBerry',
        'phantomjs': 'selenium.webdriver.PhantomJS',
        'android': 'selenium.webdriver.Android',
    }

    mod, _, cls = mapping[name].rpartition('.')
    mod = __import__(mod, fromlist=[cls])
    return getattr(mod, cls)
