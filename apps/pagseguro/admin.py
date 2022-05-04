# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from apps.curso.models import CheckoutItens
from .models import Checkout, Transaction, TransactionHistory


class CheckoutItensinLine(admin.TabularInline):
    model = CheckoutItens
    extra = 0


class CheckoutAdmin(admin.ModelAdmin):
    raw_id_fields = ['aluno']
    list_display = (
        'id',
        'aluno',
        'cpf',
        'transaction_payment_method_type',
        'transaction_status',
        'code',
        'date',
    )
    list_display_links = ('id', 'aluno')
    search_fields = ['code', ]
    list_filter = (
        'date',
        'transaction_payment_method_type',
        'transaction_status',
        ('aluno', admin.RelatedOnlyFieldListFilter)
    )
    inlines = [
        CheckoutItensinLine
    ]

class TransactionHistoryInline(admin.TabularInline):

    list_display = ('id', 'transaction', 'status', 'date')
    list_display_links = ('id', )
    search_fields = ['transaction__code', ]
    list_filter = ('status', 'date')
    model = TransactionHistory
    extra = 0


class TransactionAdmin(admin.ModelAdmin):

    list_display = ('code', 'checkout', 'reference', 'status', 'date', 'last_event_date')
    list_display_links = ('code', )
    search_fields = ['code', 'reference']
    list_filter = ('status', 'date', 'last_event_date', 'checkout')
    inlines = [
        TransactionHistoryInline
    ]


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Transaction, TransactionAdmin)
