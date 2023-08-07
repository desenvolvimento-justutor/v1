# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Aluno, FormacaoAcademica, Filtro, Mensagem, Cursos
from django.forms import ModelForm
from suit.widgets import NumberInput
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
import re


class FormacaoAcademicaForm(ModelForm):
    class Meta:
        widgets = {
            'ano_inicio': NumberInput(attrs={'class': 'input-mini'}),
            'ano_termino': NumberInput(attrs={'class': 'input-mini'})

        }


class FormacaoAcademicaInLine(admin.TabularInline):
    form = FormacaoAcademicaForm
    model = FormacaoAcademica
    extra = 0
    suit_classes = 'suit-tab suit-tab-formacao'


class FiltroInLine(admin.StackedInline):
    model = Filtro
    extra = 0
    suit_classes = 'suit-tab suit-tab-filtro'


class CursosInLine(admin.TabularInline):
    model = Cursos
    extra = 0
    suit_classes = 'suit-tab suit-tab-cursos'
    readonly_fields = ('curso', 'transaction_status')
    can_delete = False


@admin.register(Aluno)
class AlunoAdmin(AdminImageMixin, admin.ModelAdmin):
    actions = ['subscribe_aluno']
    raw_id_fields = ['usuario']
    # list_per_page = 10

    def subscribe_aluno(self, request, queryset):
        inc = 0
        total = queryset.count()
        for aluno in queryset:
            try:
                ret = aluno.subscribe()
            except Exception as e:
                self.message_user(request, "ERRO: {} -> {}".format(
                    aluno.email, str(e)
                ))
                ret = False
            if ret:
                inc += 1
        self.message_user(request, "{0} de {0} Alunos foram inscritos no Newsletter.".format(inc, total))

    def get_urls(self):
        urls = super(AlunoAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>[0-9]+)/livros/$', self.livros, name='admin-cursos-aluno'),
        ]
        return my_urls + urls

    def livros(self, request, pk):
        aluno = get_object_or_404(Aluno, id=pk)

        cpf = aluno.cpf
        if not cpf:
            cpf = ''
        context = dict(
            self.admin_site.each_context(request),
            title=aluno,
            aluno=aluno,
            senha=re.sub('[^0-9]', '', cpf)
        )
        checkouts = aluno.checkout_set.filter(transaction_status__in=[3, 4])

        livros = []
        for c in checkouts:
            for livro in c.get_livros:
                livros.append(livro)
        context['livros'] = livros
        return TemplateResponse(request, "admin-livros.html", context)

    subscribe_aluno.short_description = "Inscrever no Newsletter"

    inlines = [FormacaoAcademicaInLine, FiltroInLine, CursosInLine]
    radio_fields = {'sexo': admin.HORIZONTAL}
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['sexo', 'foto', 'usuario', 'nome', ('cpf', 'rg'), 'newsletter', 'termo']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-endereco'),
            'fields': ['cep', 'logradouro', 'numero', 'bairro', 'complemento', ('cidade', 'uf'), ('telefone', 'celular')]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-social'),
            'fields': [('email', 'email_publico'), 'url_facebook', 'url_flicker', 'url_twitter', 'url_instagram']}
         ),
        (None, {
            'classes': ('suit-tab', 'suit-tab-formacao'),
            'fields': []}
         ),
        (None, {
            'classes': ('suit-tab', 'suit-tab-filtro'),
            'fields': []}
         ),
        (None, {
            'classes': ('suit-tab', 'suit-tab-notificacao'),
            'fields': ['notificar_correcao', 'notificar_comentario', 'notificar_avaliacao', 'notificar_seguir',
                       'notificar_responder_seguir']}
         ),
        (None, {
            'classes': ('suit-tab', 'suit-tab-cursos'),
            'fields': []}
         ),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('endereco', 'Endereço'),
        ('social', 'Social'),
        ('formacao', 'Formação'),
        ('notificacao', 'Notificações'),
        ('filtro', 'Filtro'),
        ('cursos', 'Cursos'),
    )

    list_display = (
        'id',
        'nome',
        'nome_completo',
        'imagem',
        'email',
        'usuario',
        'cpf',
        'newsletter'
    )
    list_filter = ('email', 'cpf', 'newsletter')
    search_fields = ['id', 'nome', 'nome_completo', 'email', 'cpf']


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'de_aluno',
        'para_aluno'
    ]
    list_display = [
        'de_aluno',
        'para_aluno',
        'data',
        'lido'
    ]
    list_filter = [
        ('de_aluno', admin.RelatedOnlyFieldListFilter),
        ('para_aluno', admin.RelatedOnlyFieldListFilter)
    ]