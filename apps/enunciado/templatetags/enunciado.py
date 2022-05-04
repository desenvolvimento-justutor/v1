# -*- coding: utf-8 -*-
# Autor: christian
from django import template
register = template.Library()
from django.contrib.admin.templatetags import admin_modify


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_line_row(context):
    context = context or {}
    ctx = admin_modify.submit_row(context)
    if "show_save_as_duplicate" in context.keys():
        ctx["show_save_as_duplicate"] = context["show_save_as_duplicate"]
    return ctx


@register.filter(name='get_nota')
def get_nota(value, user, **kwargs):
    return 5.9
