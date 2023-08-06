import pytest
from sulfur import *


@pytest.mark.usefixtures('server')
def test_url_checker(port):
    check_ok('http://localhost:%s/base.html' % port)
    check_2xx('http://localhost:%s/base.html' % port)
    check_404('http://localhost:%s/does-not-exist.html' % port)
