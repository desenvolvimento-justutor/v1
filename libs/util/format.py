# -*- coding: utf-8 -*-
# Autor: christian
import locale
from datetime import datetime
from django.utils import timezone

def currency_format(value, symbol=True):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(float(value), symbol=symbol)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    :param time: datetime
    """
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "agora mesmo"
        if second_diff < 60:
            return str(second_diff) + " segundo(s) atrás"
        if second_diff < 120:
            return "um minuto atrás"
        if second_diff < 3600:
            return str(second_diff / 60) + " minuto(s) atrás"
        if second_diff < 7200:
            return "uma hora atrás"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hora(s) atrás"
    if day_diff == 1:
        return "Ontem"
    if day_diff < 7:
        return str(day_diff) + " dia(s) atrás"
    if day_diff < 31:
        return str(day_diff / 7) + " semana(s) atrás"
    if day_diff < 365:
        return str(day_diff / 30) + " mes(es) atrás"
    return str(day_diff / 365) + " ano(s) atrás"


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }


def timedelta_str(duration, seconds=True):
    if seconds:
        ret = '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(**convert_timedelta(duration))
    else:
        time_c = convert_timedelta(duration)
        print '>>>>>>>>', time_c
        ret = '{:02d}:{:02d}'.format(time_c['hours'], time_c['minutes'])
    return ret