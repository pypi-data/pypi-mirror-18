import pytest

from sulfur.element import Element


def test_driver_basic_functionality(driver, server_url):
    driver.open('base.html')
    assert driver.url == server_url + 'base.html'
    assert driver.title == 'Title'


def test_driver_attributes(driver):
    assert isinstance(driver.title, str)
    assert driver.page is None
    assert driver.soup is None
    assert driver.Se is driver.selenium
    assert driver.id


#
# Actions
#
def test_driver_can_finish(driver):
    driver.close()


def test_driver_can_quit(driver):
    driver.close(quit=True)


def test_driver_can_restart(driver):
    driver.restart()
    test_driver_attributes(driver)


def test_driver_back_forward(driver):
    driver.open('base.html')
    driver.open('other.html')
    driver.open('another.html')

    assert driver.title == 'Another'
    driver.back()
    assert driver.title == 'Other'
    driver.forward()
    assert driver.title == 'Another'
    driver.back(2)
    assert driver.title == 'Title'
    driver.forward(2)
    assert driver.title == 'Another'


def test_driver_executes_script(driver):
    driver.script('document.title = "changed"')
    assert driver.title == 'changed'


#@pytest.skip('TODO: async exec is halting execution')
def _test_driver_executes_async_script(driver):
    driver.script('document.title = "other"', async=True)
    driver.wait_title('other', timeout=0.5)


#
# Waits
#
def test_driver_wait_title(driver):
    dt = 0.5
    driver.open('base.html')
    driver.wait_title('Title', timeout=dt)
    driver.wait_title('itle', timeout=dt, contains=True)

    with pytest.raises(TimeoutError):
        driver.wait_title('Bad title', timeout=dt)


#
# Queries
#
def test_driver_queries(driver):
    driver.open('base.html')
    assert driver['body'] is not None
    assert len(driver('p')) == 1


#
# Cookies
#
def test_driver_cookie_interface(driver):
    driver.open('base.html')
    assert len(driver.cookies) == 0


#TODO: make cookie?
def _test_driver_can_create_cookie(driver):
    driver.cookies.create('foo', d1=41, d2=42)
    assert len(driver.cookies) == 1
    assert driver.cookies['foo']['d2'] == 42
    driver.cookies.clear()
    assert len(driver.cookies) == 0


#
# Screenshots
#
def test_can_take_screenshot(driver):
    if not driver.windowless:
        F = driver.screenshot()
        data = F.read()
        assert data[:6] == b'\x89PNG\r\n'


#
# Windows
#
def test_window_operations(driver):
    driver.window.shape = 800, 600
    assert driver.window.shape == (800, 600)
    driver.window.maximize()


#
# Focus
#
def test_focus_manager(driver):
    if not driver.windowless:
        driver.open('base.html')
        driver.switch_to.window()
        assert isinstance(driver.switch_to.active(), Element)
        assert driver.switch_to.alert() is None
