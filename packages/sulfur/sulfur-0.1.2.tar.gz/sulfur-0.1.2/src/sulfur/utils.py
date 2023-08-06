def normalize_url(url):
    """
    Forces url to have a correct protocol specification.

    Examples:
        >>> normalize_url('google.com')
        'http://google.com'
    """

    if '://' not in url:
        return 'http://' + url
    return url
