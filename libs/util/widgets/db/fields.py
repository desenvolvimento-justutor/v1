#coding:utf8
from django.forms import CharField, FloatField


class ZMoneyField(FloatField):
    def __init__(self, *args, **kwargs):
        super(ZMoneyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        np = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']
        if type(value) not in [str, unicode]: value = '%.4f' % value
        for i in value:
            if i not in np:
                value = value.replace(i, '')
        try: value = value.replace('.', '').replace(',', '.')
        except: pass
        return value


class ZMaskedField(CharField):
    def __init__(self, *args, **kwargs):
        super(ZMaskedField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        np = ['(', ')', '-', '.', '/', ' ']
        if value:
            for i in np: value = value.replace(i, '')
        return value


class ZColorPickerField(CharField):
    def to_python(self, value):
        return value