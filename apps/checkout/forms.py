# -*- coding: utf-8 -*-
# @Filename : forms
# @Date : 2019-12-16-05-59
# @Poject: justutor
# @AUTHOR : Christian Douglas <christian.douglas.alcantara@gmail.com>
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from decimal import Decimal


class CartForm(forms.Form):
    codigo = forms.CharField(
        max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',  'placeholder': "Código", 'required': 'required'})
    )
    remover = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class AlunoForm(forms.Form):
    pass
