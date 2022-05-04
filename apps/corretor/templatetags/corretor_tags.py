# -*- coding: utf-8 -*-
# Autor: christian
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(takes_context=True)
def initial_letter_filter(solicitacao, user):
    css_class = 'hide'
    if solicitacao.corretores.filter(id=user.corretor.id).first():
        css_class = 'fa fa-2x fa-star'
    result = '<i style="color: #FFC107" class="%s" data-toggle="tooltip" data-original-title="Favorito"></i>' % css_class
    return mark_safe(result)
