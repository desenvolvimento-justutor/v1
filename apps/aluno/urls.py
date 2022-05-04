# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'apps.aluno.views',
    url(r'^painel/$', 'painel', name='painel'),
    url(r'^relatorio/$', 'relatorio', name='relatorio'),
    url(r'^lista/$', 'lista', name='lista'),
    url(r'^producao/$', 'perfil', name='perfil'),
    url(r'^cursos/$', 'cursos', name='cursos'),
    url(r'^simulados/$', 'simulados', name='simulados'),
    url(r'^simuladoinfo/(?P<pk>[-\w]+)/$', 'simuladoinfo', name='simuladoinfo'),
    url(r'^simulado/', include('apps.autor.urls', namespace='simulado')),
    url(r'^gabaritos-autocorrecao/$', 'gabarito_autocorrecao', name='gabaritos_autocorrecao'),
    # financeiro
    url(r'^creditos/$', 'creditos', name='creditos'),
    url(r'^creditos/comprar/$', 'creditos_comprar', name='creditos_comprar'),
    url(r'^creditos/comprar/render/$', 'creditos_comprar_render', name='creditos_comprar_render'),
    url(r'^creditos/resgates/$', 'creditos_resgates', name='creditos_resgate'),
    url(r'^creditos/historico/$', 'creditos_historico', name='creditos_historico'),
    # gabarito
    url(r'^gabaritos-autocorrecao/formulario/(?P<pk>[0-9]+)/$', 'gabarito_autocorrecao_formulario',
        name='gabaritos_autocorrecao_formulario'),
    url(r'^gabaritos-autocorrecao/formulario/(?P<pk>[0-9]+)/corrigir/$', 'gabarito_autocorrecao_formulario_corrigir',
        name='gabaritos_autocorrecao_formulario_corrigir'),
    url(r'^cupons/$', 'cupons', name='cupons'),
    url(r'^livros/$', 'livros', name='livros'),
    url(r'^baixar_livro/(?P<lid>[-\w]+)/$', 'baixar_livro', name='baixar-livro'),
    url(r'^certificado/$', 'certificado', name='certificado'),
    url(r'^certificado/solicitar/(?P<cid>[-\w]+)/$', 'certificado_solicitar', name='certificado-solicitar'),

    url(r'^sentencas-avulsas/$', 'sentencas_avulsas', name='sentencas-avulsas'),
    url(r'^sentencas-oab/$', 'sentencas_oab', name='sentencas-oab'),

    url(r'^cursos/video/(?P<vid>[-\w]+)/$', 'video', name='curso-video'),
    url(r'^cursos/discussao/(?P<pk>[-\w]+)/$', 'discussao', name='curso-discussao'),
    url(r'^perfil-aluno/(?P<aid>[-\w]+)/$', 'perfil_aluno', name='perfil-aluno'),
    url(r'^busca/$', 'busca_aluno', name='busca-aluno'),
    url(r'^notificacoes/$', 'notificacoes', name='notificacoes'),
    url(r'^timeline/$', 'timeline', name='timeline'),
    url(r'^mensagens/$', 'mensagens', name='mensagens'),
    url(r'^configuracoes/$', 'configuracoes', name='configuracoes'),
    url(r'^get_message/$', 'get_message', name='get_message'),
    url(r'^busca-aluno-json/$', 'busca_aluno_json', name='busca-aluno-json'),

    url(r'^cadastro/$', 'cadastro', name='cadastro'),
    url(r'^meus-desafios/$', 'meus_desafios', name='meus-desafios'),
)
