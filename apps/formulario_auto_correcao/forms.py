# -*- coding: utf-8 -*-
from django.forms import modelformset_factory, inlineformset_factory, ModelForm
from .models import Formulario, Tabela

class FormularioForm(ModelForm):
    class Meta:
        model = Formulario
        exclude = ()

FormularioFormSet = inlineformset_factory(
    Formulario,
    Tabela,
    form=FormularioForm,
)