# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url

from .views import relatorio

app_name = "formulario_correcao"

urlpatterns = patterns(
    'apps.formulario_correcao.views',
    url(r'^relatorio/$', relatorio, name='relatorio'),
)
