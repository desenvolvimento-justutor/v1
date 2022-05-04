# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'apps.quizz.views',
    url(r'^(?P<pk>\d+)/$', views.quizz, name='quizz'),
    url(r'^questao/(?P<qpk>\d+)/(?P<pk>\d+)/$', views.questao, name='questao'),
)
