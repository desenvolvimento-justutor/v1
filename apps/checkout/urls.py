# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url
from .views import (
    CartView, PersonalInfomationView,
    PaymentView, StatusView, StatusPixView,
    ajax_cupom_actions,
    ajax_get_cob,
    ajax_busca_cep,
    ajax_checkout,
    ajax_check_checkout
)


urlpatterns = patterns(
    'apps.checkout.views',
    url(r'^carrinho/$', CartView.as_view(), name='cart'),
    url(r'^dados-pessoais/$', PersonalInfomationView.as_view(), name='personal_information'),
    url(r'^pagar/$', PaymentView.as_view(), name='payment'),
    url(r'^status/(?P<code>[-\w]+)/$', StatusView.as_view(), name='status'),
    url(r'^status/pix/(?P<code>[-\w]+)/$', StatusPixView.as_view(), name='status-pix'),
    #url(r'^transaction/(?P<code>[a-f0-9]{8}-?[a-f0-9]{5}-?[a-f0-9]{4}-?[89ab][a-f0-9]{17})/$', ConfirmationView.as_view(), name='confirmation'),
    # ajax
    url(r'^ajax_cupom_actions/$', ajax_cupom_actions, name='ajax_cupom_actions'),
    url(r'^ajax_get_cob/$', ajax_get_cob, name='ajax_get_cob'),
    url(r'^ajax_busca_cep/$', ajax_busca_cep, name='ajax_busca_cep'),
    url(r'^ajax_checkout/$', ajax_checkout, name='ajax_checkout'),
    url(r'^ajax_check_checkout/$', ajax_check_checkout, name='ajax_check_checkout'),
)
