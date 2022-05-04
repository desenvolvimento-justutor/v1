# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    'apps.formulario_auto_correcao.views',
    url(r'^ajax_responder/$', views.ajax_responder, name='responder'),
    url(r'^baixar_correcao/(?P<pk>[0-9]+)/$', views.baixar_correcao, name='baixar_correcao'),
)
