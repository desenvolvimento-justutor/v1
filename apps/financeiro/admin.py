# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from suit.widgets import SuitSplitDateTimeWidget

from .models import Credito, CreditoResgate, ConfiguracaoPacote, Pacote, PacoteDesconto


class PacoteDescontoInLine(admin.StackedInline):
    model = PacoteDesconto
    extra = 0
    suit_classes = 'suit-tab suit-tab-desconto'


class CreditoResgateInline(admin.TabularInline):
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }
    model = CreditoResgate
    extra = 0


class PacoteInline(admin.TabularInline):
    model = Pacote
    extra = 0
    suit_classes = 'suit-tab suit-tab-pacote'


@admin.register(ConfiguracaoPacote)
class ConfiguracaoPacoteAdmin(admin.ModelAdmin):
    inlines = [
        PacoteInline, PacoteDescontoInLine
    ]
    list_display = [
        'titulo',
        'curso',
        'created',
        'valor_unitario',
        'qtda_min',
        'qtda_max',
        'ativo'
    ]
    list_filter = [
        'ativo'
    ]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': [
                'ativo',
                'curso',
                'titulo',
                'valor_unitario',
                ('qtda_min', 'qtda_max')
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-pacote'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-desconto'),
            'fields': []
        })
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('pacote', 'Pacote'),
        ('desconto', 'Desconto'),
    )


@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'aluno'
    ]
    list_display = [
        u'uuid',
        u'aluno',
        u'created',
        u'quantidade',
        u'expire_date',
        u'origem',
    ]

    list_filter = [
        ('aluno', admin.RelatedOnlyFieldListFilter),
        'quantidade',
        'expire_date',
        'origem'
    ]
    radio_fields = {
        'origem': admin.HORIZONTAL
    }
    inlines = [
        CreditoResgateInline
    ]


@admin.register(CreditoResgate)
class CreditoResgateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }
    list_display = (
        u'credito',
        u'created',
        u'modified',
        u'quantidade'
    )
    list_filter = [
        'credito'
    ]
