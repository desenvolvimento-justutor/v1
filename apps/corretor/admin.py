# -*- coding: utf-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Corretor, Banco


class BancoInLine(admin.StackedInline):
    model = Banco
    extra = 0
    suit_classes = 'suit-tab suit-tab-banco'


@admin.register(Corretor)
class CorretorAdmin(AdminImageMixin, admin.ModelAdmin):

    inlines = [BancoInLine]
    filter_horizontal = ['disciplinas']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['nome', ('cpf', 'rg'), 'pis', 'email', ('ddd_telefone', 'telefone'),
                       ('ddd_celular', 'celular')]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-perfil'),
            'fields': ['user', 'foto', 'ocupacao', 'curriculo', 'questao', 'peca', 'sentenca', 'disciplinas']}
         ),
        (None, {
            'classes': ('suit-tab', 'suit-tab-endereco'),
            'fields': ['cep', 'logradouro', 'numero', 'bairro', 'complemento', ('cidade', 'uf'),
                       ('telefone', 'celular')]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-banco'),
            'fields': []
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('perfil', 'Perfil'),
        ('endereco', 'Endereço'),
        ('banco', 'Banco'),
    )

    list_display = ('nome', 'email', 'user', 'cpf', 'data_cadastro')
    list_filter = ('user', 'email', 'cpf')
    search_fields = ['nome']
