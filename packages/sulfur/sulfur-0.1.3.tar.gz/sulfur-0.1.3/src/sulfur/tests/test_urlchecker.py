import pytest

from sulfur import check_server_error, check_client_error, check_success, \
    check_2xx, check_ok, check_4xx, check_3xx, check_404, check_5xx, \
    ValidationError


@pytest.fixture
def url(port):
    return 'http://localhost:%s/base.html' % port


def test_url_checker(server, url):
    assert check_ok(url)
    assert check_success(url)
    assert check_2xx(url)
    assert not check_4xx(url)
    assert not check_3xx(url)
    assert not check_client_error(url)
    assert not check_server_error(url)
    assert check_404(server.base_url + 'does-not-exist.html')


def test_raises_on_error(url):
    with pytest.raises(ValidationError):
        check_server_error(url, raises=True)


def test_check_valid_html5(server):
    assert check_ok(server.base_url + 'base.html', html5=True)
    assert not check_ok(server.base_url + 'bad.html', html5=True)
    with pytest.raises(ValidationError):
        check_ok(server.base_url + 'bad.html', html5=True, raises=True)


def test_failed_post(url):
    assert check_5xx(url, post={'foo': 'bar'})


def test_multiple_urls(url, port):
    urls = [url, url[:-9] + 'bad.html']
    assert check_ok(urls)
    assert not check_ok(urls, html5=True)
