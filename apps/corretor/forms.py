# -*- coding: utf-8 -*-
# Autor: christian
from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Corretor


class FormCorretor(ModelForm):
    class Meta:
        model = Corretor
        fields = '__all__'

        widgets = {
            'disciplinas': CheckboxSelectMultiple()
        }