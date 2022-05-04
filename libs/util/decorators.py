# coding=utf-8
from django.http import HttpResponse


def threaded(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl

    return async_func

ACC_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}

def cross_domain_ajax(func):
    """ Sets Access Control request headers."""
    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS":
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.iteritems():
            response[k] = v
        return response
    return wrap
