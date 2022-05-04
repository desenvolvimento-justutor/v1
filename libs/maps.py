# -*- coding: utf-8 -*-

__author__ = 'christian'


import urllib
import urlparse
import json

URL_GOOGLE = "http://maps.google.com/maps/api/geocode/json?address="


def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


def get_json_map(endereco='', numero='', bairro='', cidade='', uf=''):
    url = URL_GOOGLE + '+'.join(endereco.split()) + '&sensor=false&output=embed"'
    f = urllib.urlopen(url_fix(url))
    contents = json.load(f)
    f.close()
    return contents

