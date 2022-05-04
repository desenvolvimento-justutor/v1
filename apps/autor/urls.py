# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns(
    'apps.autor.views',
    url(r'^questionario/(?P<pk>[-\w]+)/$', views.questionario, name='questionario'),
    url(r'^ajax-responder/', views.ajax_responder, name='ajax-responder'),
    url(r'^ajax-questao-render/', views.ajax_questao_render, name='ajax-questao-render'),
    url(r'^ajax-update-timer/', views.ajax_update_timer, name='ajax-update-timer'),
    url(r'^ajax-check-time/', views.ajax_check_time, name='ajax-check-time'),
    url(r'^ajax-check-time/', views.ajax_check_time, name='ajax-check-time'),
    url(r'^ajax-encerrar-simulado/', views.ajax_encerrar_simulado, name='ajax-encerrar-simulado'),
    url(r'^ajax-render-comentario/', views.ajax_render_comentario, name='ajax-render-comentario'),
    url(r'^ajax-render-html/$', views.ajax_render_html, name='ajax-render-html'),
    url(r'^ajax-modal-estatisticas/$', views.ajax_modal_estatisticas, name='ajax-modal-estatisticas'),
)
