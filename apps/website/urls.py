# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    'apps.website.views',
    url(r'^$', 'index', name='index'),
    url(r'^professores/$', views.ProfessorView.as_view(), name='professores'),
    url(r'^institucional/(?P<slug>[-\w]+)/$', 'institucional', name='institucional'),
    url(r'^livraria/(?P<slug>[-\w]+)/$', 'livraria', name='livraria'),
    url(r'^livraria/livro/(?P<slug>[-\w]+)/$', 'livro', name='livro'),
    url(r'^noticia/(?P<slug>[-\w]+)/$', 'noticia', name='noticia'),
    url(r'^consulta-certificado/(?P<chave>[-\w]+)/$', 'consulta_certificado', name='consulta-certificado'),
    url(r'^php/handler.php$', 'subscrible', name='subscrible'),
    url(r'^imagens/$', 'imagens', name='imagens'),
    # url(r'^videos-justutor/$', 'videos_justutor', name='videos-justutor'),
    url(r'^noticias-justutor/$', 'noticias_justutor', name='noticias-justutor'),
    url(r'^artigo-indice$', 'artigo_indice', name='artigo-indice'),
    url(r'^artigo-imprimir/(?P<aid>[-\w]+)/$', 'artigo_imprimir', name='artigo-imprimir'),
    # url(r'^social-login/completo/(?P<backend>[^/]+)/$', 'login_completo', name='login_completo'),
    url(r'^busca/$', 'busca', name='busca'),
    url(r'^busca-aluno/$', 'busca_aluno', name='busca-aluno'),
    url(r'^busca-tag/$', 'busca_tag', name='busca-tag'),
    url(r'^check-login/$', 'check_login', name='check-login'),
    url(r'^ajax-login/$', 'ajax_login', name='ajax-login'),
    url(r'^ajax-cadastro/$', 'ajax_cadastro', name='ajax-cadastro'),
    url(r'^email/$', 'email', name='email'),
    url(r'^pagseg/checkout/$', 'pagseguro_checkout', name='pagseguro_checkout'),
    url(r'^pagseg/settransaction/$', 'pagseguro_set_transaction', name='pagseguro_settransaction'),
    url(r'^pagseg/transacao/(?P<code>[-\w]+)/$', 'pagseguro_transaction', name='pagseguro_transaction'),
    url(r'^pagseg/transacao/$', 'pagseguro_transaction', name='pagseguro_transaction_nocode'),

    url(r'^checkout/itens/$', 'checkout_itens', name='checkout_itens'),
    url(r'^checkout/pagamento/$', 'checkout_itens', name='checkout_pagamentos'),
    url(r'^whatsapp/$', 'whatsapp', name='whatsapp'),
    url(r'^whatsapp/inscrever/$', 'whatsapp_inscrever', name='whatsapp-inscrever'),
)

urlpatterns += [
    url(r'^v2/$', views.HomeView.as_view(), name='home')
]