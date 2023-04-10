# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Cobranca


@admin.register(Cobranca)
class CobrancaAdmin(admin.ModelAdmin):
    list_display = (
        "get_aluno",
        "get_cpf",
        "data",
        "valor",
        "status"
    )
    list_filter = ("data", "status")
    search_fields = ("checkout", "checkout__aluno", "checkout__cpf")

    def get_aluno(self, obj):
        return obj.checkout.aluno

    def get_cpf(self, obj):
        return obj.checkout.cpf

    get_aluno.short_description = 'Aluno'
    get_aluno.admin_order_field = 'checkout__aluno'
    get_cpf.short_description = 'CPF'
    get_cpf.admin_order_field = 'checkout__cpf'
