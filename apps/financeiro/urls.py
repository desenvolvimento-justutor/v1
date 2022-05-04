# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    'apps.financeiro.views',
    # financeiro
    url(r'^teste/$', views.teste, name='teste'),
    url(r'^get-credito/$', views.get_credito, name='get-credito'),
)
