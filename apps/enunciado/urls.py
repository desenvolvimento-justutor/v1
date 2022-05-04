# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.enunciado.views',
    url(r'^(?P<ptipo>questao|peca|sentenca)/$', 'tipo', name='tipo'),
    url(r'^(?P<ptipo>questao|peca|sentenca)/(?P<pid>[-\w]+)/$', 'tipo', name='tipo-id'),
    url(r'^(?P<ptipo>questao|peca|sentenca)/(?P<pid>[-\w]+)/responder/$', 'responder', name='responder'),
    # Resposta
    url(r'^imprimir/(?P<eid>[-\w]+)/$', 'imprimir', name='imprimir'),
    url(r'^resposta/(?P<rid>[-\w]+)/$', 'resposta', name='resposta'),
    url(r'^socilitar-correcao/(?P<rid>[-\w]+)/$', 'solicitar_correcao', name='solicitar-correcao'),

    url(r'^roteiros/$', 'roteiros', name='roteiros'),
    url(r'^roteiro/(?P<slug>[-\w]+)/$', 'roteiro', name='roteiro'),
    url(r'^roteiro/(?P<slug>[-\w]+)/(?P<item_slug>[-\w]+)/$', 'roteiro_item', name='roteiro-item'),
    url(r'^roteiro/(?P<slug>[-\w]+)/(?P<item_slug>[-\w]+)/(?P<sub_slug>[-\w]+)/$', 'roteiro_subitem', name='roteiro-sub-item'),

    url(r'^avaliar-correcao/', 'avaliar_correcao', name='avaliar-correcao'),
    url(r'^avaliar-resposta/(?P<rid>[-\w]+)/', 'avaliar_resposta', name='avaliar-resposta'),
    # Correção
    url(r'^correcao/(?P<cid>[-\w]+)/$', 'correcao', name='correcao'),
    # Últimas postagens
    url(r'^atividade/', 'atividade', name='atividade'),
    url(r'^temas-abordados/', 'temas_abordados', name='temas-abordados'),
    url(r'^mais-populares/', 'mais_populares', name='mais-populares'),

    url(r'^resposta-desativar/(?P<rid>[-\w]+)/$', 'resposta_desativar', name='resposta-desativar'),
    url(r'^resposta/(?P<pid>[-\w]+)/(?P<cid>[-\w]+)/$', 'resposta', name='correcao'),

    url(r'^ranking/$', 'ranking', name='ranking'),
    url(r'^ranking-premiado/$', 'ranking_premiado', name='ranking-premiado'),
    url(r'^get_chart/$', 'get_chart', name='get-chart'),

    url(r'^busca/$', 'busca', name='busca'),
    url(r'^get/$', 'obter', name='obter'),

    url(r'^salvar-resposta/$', 'salvar_resposta', name='salvar-resposta'),
    url(r'^recentes/$', 'recentes', name='recentes'),

)
