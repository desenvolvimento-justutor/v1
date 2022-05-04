# -*- coding: utf-8 -*-
# Autor: christian
from __future__ import unicode_literals
from django.contrib import admin

from .models import Professor, Mensagem


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'graduacao', 'user', 'publico']
    search_fields = ['nome']


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ['professor', 'aluno', 'curso', 'data', 'lido']
    search_fields = ['aluno__nome', 'mensagem']
    list_filter = ['professor', 'curso', 'data', 'lido']
    raw_id_fields = ['curso', 'aluno']




