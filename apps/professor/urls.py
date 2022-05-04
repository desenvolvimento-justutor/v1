# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    'apps.professor.views',
    url(r'^$', views.painel, name='painel'),
    url(r'^cursos/$', views.cursos, name='cursos'),
    url(r'^sentencas/$', views.sentencas, name='sentencas'),
    url(r'^sentencas/view/(?P<pk>\d+)/$', views.sentenca_view, name='sentenca_view'),
    url(r'^recursos/$', views.recursos, name='recursos'),
    url(r'^sentencas-oab/$', views.sentencas_oab, name='sentencas-oab'),
    url(r'^mensagens$', views.mensagens, name='mensagens'),
    url(r'^mensagens/(?P<pk>[-\w]+)/$', views.mensagens, name='mensagens-curso'),
    url(r'^get-message/$', views.get_message, name='get-message'),
    url(r'^redigir-correcao/(?P<pk>\d+)/$', views.redigir_correcao, name='redigir-correcao'),
    url(r'^formulario-correcao/(?P<pk>\d+)/$', views.formulario_correcao, name='formulario-correcao'),
    url(r'^formulario-correcao-sentenca/(?P<pk>\d+)/$', views.formulario_correcao_sentenca,
        name='formulario-correcao-sentenca'),
    url(r'^get-sentenca-aluno/(?P<pk>\d+)/$', views.get_sentenca_aluno, name='get-sentenca-aluno'),

    url(r'^formulario-estatistica/$', views.formulario_estatistica, name='formulario-estatistica'),
    url(r'^formulario-estatistica-geral/$', views.formulario_estatistica_geral, name='formulario-estatistica-geral'),
    url(r'^formulario-recorrer/$', views.formulario_recorrer, name='formulario-recorrer'),
    url(r'^formulario-estatistica-sentenca/$', views.formulario_estatistica_sentenca,
        name='formulario-estatistica-sentenca'),

    url(r'^formulario-estatistica-correcao/$', views.formulario_estatistica_correcao,
        name='formulario-estatistica-correcao'),
    url(r'^corecao-get-data/$', views.correcao_get_data, name='correcao-get-data'),
    url(r'^post-salvar-tabela/$', views.post_salvar_tabela, name='post-salvar-tabela'),
    url(r'^post-salvar-comentario/$', views.salvar_comentario_professor, name='post-salvar-comentario'),
    url(r'^post-salvar-item/$', views.salvar_item_recorrer, name='post-salvar-item'),
    url(r'^post-confirmar-recorer/$', views.post_confirmar_recorrer, name='post-confirmar-recorrer'),
    # url(r'^email/$', 'email', name='email'),
)
