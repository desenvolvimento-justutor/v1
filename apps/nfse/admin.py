# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import NSFe


class NSFeAdmin(admin.ModelAdmin):

    list_display = (
        u'ref',
        u'aluno',
        u'data_emissao',
        u'status',
    )
    list_filter = ('status', u'data_emissao')
    raw_id_fields = ("aluno",)

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


admin.site.register(NSFe, NSFeAdmin)
