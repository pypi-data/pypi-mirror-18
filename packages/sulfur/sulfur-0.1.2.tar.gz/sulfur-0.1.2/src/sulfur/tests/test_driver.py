def test_driver(driver):
    driver.open()
    assert 'listing' in driver.title
