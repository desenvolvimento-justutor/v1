# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'apps.corretor.views',
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^painel/$', views.painel, name='painel'),
    url(r'^pregao/$', views.pregao, name='pregao'),
)
