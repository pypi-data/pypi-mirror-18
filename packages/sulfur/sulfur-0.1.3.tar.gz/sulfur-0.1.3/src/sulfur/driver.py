import io

from bs4 import BeautifulSoup
from lazyutils import lazy, delegate_to
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sulfur.driver_attributes import WindowManager, FocusManager, CookieManager
from sulfur.element import Element
from sulfur.id_manager import IdManager
from sulfur.queriable import QueriableMixin
from sulfur.query import Query
from sulfur.utils import normalize_url, join_url, wraps_selenium_timeout_error


class DriverBase(QueriableMixin):
    """
    A simplified interface to the selenium webdriver with simpler method names
    and a few useful resources.
    """

    _soup_lib = 'html5lib'

    title = delegate_to('_driver')

    @lazy
    def cookies(self):
        """
        Access and modify cookies.
        """

        return CookieManager(self)

    @property
    def selenium(self):
        """
        Selenium web driver object.
        """

        return self._driver

    @property
    def Se(self):
        """
        Alias to .selenium
        """

        return self.selenium

    @lazy
    def soup(self):
        """
        A beautiful soup interface to the HTML source code
        """

        if self.page is None:
            return None
        else:
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

    @property
    def version(self):
        """
        Browser's version.
        """

        return self._driver.capabilities['version']

    @property
    def html(self):
        """
        Page's html source code.
        """

        return self._driver.page_source

    @property
    def window(self):
        """
        Control window behaviors.
        """

        return WindowManager(self)

    @property
    def switch_to(self):
        """
        Focus manager.
        """

        return FocusManager(self)

    @property
    def windowless(self):
        """
        True if driver runs on a windowless mode (e.g., phantomjs).
        """

        return self._driver.name in ['phantomjs']

    def __init__(self, driver, url='', wait=0):
        self._driver = driver
        self._page = None
        self.base_url = url and normalize_url(url)
        self.url = None
        self._driver.implicitly_wait(wait)
        if url:
            self.open()

    def __call__(self, selector):
        return self.query(selector)

    def __getitem__(self, selector):
        return self.get(selector)

    # Browser actions
    def open(self, url=''):
        """
        Opens the given url.

        Returns a page object.
        """

        self.url = join_url(self.base_url, url)
        return self._driver.get(self.url)

    def back(self, n=1):
        """
        Go back n steps in browser history.
        """

        if n >= 1:
            self._driver.back()
            self.back(n - 1)
        elif n < 0:
            self._driver.forward()
            self.back(n + 1)

    def forward(self, n=1):
        """
        Go forward n steps in browser history.
        """

        self.back(-n)

    def refresh(self):
        """
        Refresh current page.
        """

        self._driver.refresh()

    def click(self, selector):
        """
        Clicks in the first element with the given CSS selector.
        """

        elem = self.get(selector)
        if elem is not None:
            elem.click()

    def send(self, *args, to=None):
        """
        Alias to send_keys().
        """

        return self._driver.send_keys(*args)

    def script(self, script, async=False):
        """
        Executes JavaScript script.

        Args:
            script (str):
                A string of JavaScript source.
            async (bool):
                Set to True to execute script asyncronously.
        """

        if async:
            self._driver.execute_async_script(script)
        else:
            self._driver.execute_script(script)

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

    def restart(self):
        """
        Restart the web driver and go to the current url.
        """

        self._driver = type(self._driver)()
        self.open(self.url or '')

    # Other
    def screenshot(self, path=None, format='png'):
        """
        Returns a file object holding data for a  screenshot of the current
        screen.

        Args:
            path:
                If given, saves file in the given path.
            format:
                One of 'png' or 'base64'
        """

        if path:
            F = open(path, 'wb')
        else:
            F = io.BytesIO()

        if format == 'png':
            data = self._driver.get_screenshot_as_png()
        elif format == 'base64':
            data = self._driver.get_screenshot_as_base64()
        else:
            raise ValueError('invalid format: %r' % format)
        F.write(data)
        return F

    # Wait conditions
    @wraps_selenium_timeout_error
    def wait(self, func, timeout=1.0):
        """
        Wait until func(driver) return True.

        Raises a TimeoutError if condition is not met in the given timeout
        interval.
        """

        WebDriverWait(self, timeout).until(func)

    @wraps_selenium_timeout_error
    def wait_title(self, value, timeout=1.0, contains=False):
        """
        Waits until the page title assumes the given value.

        Raises a TimeoutError if condition is not met in the given interval.

        Args:
            value (str):
                expected title
            timeout (float):
                timeout in seconds
            contains (bool):
                If true, checks if title contains the value substring. The
                default behavior is to wait until the title is exactly equal
                the given value string.
        """

        if contains:
            condition = EC.title_contains(value)
        else:
            condition = EC.title_is(value)
        WebDriverWait(self, timeout).until(condition)

    # Private methods
    def _wrap_element(self, element):
        return Element(element, self)

    def _wrap_query(self, query):
        wrap = self._wrap_element
        return Query(self, [wrap(x) for x in query])

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
