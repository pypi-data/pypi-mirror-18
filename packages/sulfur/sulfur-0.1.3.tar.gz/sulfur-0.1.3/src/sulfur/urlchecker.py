from sulfur.client import Client
from sulfur.errors import ValidationError


def check_response(url, url_data=None,
                   method=None, post=None,
                   login=None, login_required=False,
                   codes=None, code_checker=None,
                   html5=False, html5_validator=None,
                   xhtml=False,
                   client=None,
                   raises=False):
    """
    Check if response obey certain constraints.

    Args:
        url (str):
            Page's url. It uses url_data to format the url as
            ``url.format(**url_data)``. If a list of urls is given, it tests each
            url separately.
        url_data (dict):
            A dictionary used to format url strings.
        method (str):
            HTTP method used to retrieve page. (default: 'GET').
        post (dict):
            A dictionary with post data. If given, makes method='POST'.
        codes (sequence):
            a list of allowed HTTP response codes.
        code_checker (function):
            a function that checks if the response code is valid or not.
        login (str or tuple):
            Can be either a username or a tuple with (username, password) used
            to login just before making the request.
        login_required (bool):
            If True, anonymous users must either return a 401, 403, 404 or it
            must be a redirect to a login page.
        html5 (bool):
            If True, makes sure that the response is valid HTML5.
        html5_validator:
            Method used to validate the HTML5 code.
        xhtml (bool):
            If True, makes sure the response is valid XHTML.
        raises (bool):
            If True, raises an exception instead of returing False.

    Raises:
        If check fails, raises an AssertionError.
    """

    # If a list of urls is given, call check_response() in each element
    # separately
    if not isinstance(url, (str, bytes)):
        kwargs = locals()
        del kwargs['url']
        for url_item in url:
            if not check_response(url_item, **kwargs):
                return False
        return True

    # Format url using url_data
    if url_data:
        url = url.format(**url_data)

    # Makes login, if necessary
    client = _get_client_object(client)
    if login:
        if isinstance(login, (tuple, list)):
            username, password = login
            client.login(username=username, password=password)
        else:
            client.force_login(login)

    # Build kwargs for executing client's .get(), .post() or other HTTP methods
    client_kwargs = {}
    if post and method is None:
        method = 'POST'
    elif method is None:
        method = 'GET'
    if method == 'POST' and post:
        client_kwargs['data'] = post

    # Fetch data from server object
    http_method = getattr(client, method.lower())
    response = http_method(url, **client_kwargs)
    response_data = response.content

    # Normalize code checker to be a function that returns True on valid
    # response codes. Check if status code is valid
    if codes and not code_checker:
        def code_checker(code):
            return code in codes
    if not code_checker:
        def code_checker(code):
            return True
    status_code = response.status_code
    if not code_checker(status_code):
        if raises:
            raise ValidationError('%s: received invalid status code: %s' %
                                  (url, status_code))
        else:
            return False

    # Now we check if the content HTML data validates
    if html5:
        html5_validator = _get_html5_validator(html5_validator)
        try:
            html5_validator(response_data)
        except ValidationError as ex:
            if raises:
                raise ValidationError('%s: %s' % (url, ex))
            else:
                return False
    return True


def _get_client_object(server, **kwargs):
    """
    Return the server object from request.
    """

    if server is not None:
        return server

    return Client(**kwargs)


def _get_html5_validator(html5_validator):
    """
    Normalize the html5_validator parameter from check_response.
    """

    from sulfur.validators import Html5Validator

    if html5_validator is None:
        html5_validator = 'default'
    if callable(html5_validator):
        return html5_validator
    return Html5Validator.as_validator(html5_validator)


def check_ok(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is either in the
    2xx or in the 3xx range.
    """

    return check_response(url,
                          code_checker=lambda code: 200 <= code <= 399,
                          **kwargs)


def check_2xx(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is in the 2xx
    range.
    """

    return check_response(url,
                          code_checker=lambda code: 200 <= code <= 299,
                          **kwargs)


def check_3xx(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is in the 3xx
    range.
    """

    return check_response(url,
                          code_checker=lambda code: 300 <= code <= 399,
                          **kwargs)


def check_4xx(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is in the 4xx
    range.
    """

    return check_response(url,
                          code_checker=lambda code: 400 <= code <= 499,
                          **kwargs)


def check_404(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is 404.
    """

    return check_response(url, codes=[404], **kwargs)


def check_5xx(url, **kwargs):
    """
    Like :func:`check_response`, but checks if response code is in the 5xx
    range.
    """

    return check_response(url,
                          code_checker=lambda code: 500 <= code <= 599,
                          **kwargs)


# Aliases
def check_success(url, **kwargs):
    """
    Alias to :func:`check_2xx`.
    """
    return check_2xx(url, **kwargs)


def check_redirect(url, **kwargs):
    """
    Alias to :func:`check_3xx`.
    """
    return check_3xx(url, **kwargs)


def check_client_error(url, **kwargs):
    """
    Alias to :func:`check_4xx`.
    """
    return check_4xx(url, **kwargs)


def check_server_error(url, **kwargs):
    """
    Alias to :func:`check_5xx`.
    """
    return check_5xx(url, **kwargs)

