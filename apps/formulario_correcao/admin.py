# -*- coding: utf-8 -*-
import copy

from django.contrib import admin
from django.contrib import messages
from django.db import models
from django.forms import ModelForm
from django.shortcuts import redirect
from redactor.widgets import RedactorEditor
from suit.admin import SortableStackedInline, SortableModelAdmin
from suit.widgets import AutosizedTextarea, TextInput

from .models import Nota, Formulario, Tabela, TabelaCorrecaoAluno, TabelaAluno
from django.contrib import messages


class NotaFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'titulo': TextInput(attrs={'class': 'span12'}),
            'texto': RedactorEditor(),
        }


class TabelaFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'item': AutosizedTextarea(attrs={'rows': 2, 'class': 'span12'}),
            'comentarios': RedactorEditor(),
        }


class FormularioFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'titulo': TextInput(attrs={'class': 'span12'}),
            'texto': RedactorEditor()
        }


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    form = NotaFormAdmin
    list_display = ['titulo', 'valor', "unica"]
    search_fields = ['texto', 'titulo']
    fields = ["titulo", "unica", "texto", "valor"]

    def _copy(self, request, pk):
        nota = Nota.objects.get(pk=pk)
        nota_cp = copy.copy(nota)
        nota_cp.id = None
        nota_cp.titulo = u'Cópia: {}'.format(nota.titulo)
        nota_cp.texto = nota.texto
        nota_cp.valor = nota.valor
        nota_cp.save()

        messages.success(request, u"{0}, Duplicado com sucesso.".format(nota_cp))
        return redirect('/admin/formulario_correcao/nota/%s/' % nota_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(NotaAdmin, self).response_change(request, obj)


class TabelaAdminInline(SortableStackedInline):
    classes = ['collapse']
    filter_horizontal = ['nota']
    form = TabelaFormAdmin
    model = Tabela
    extra = 0
    fields = [
        'item', 'valor',  # , 'comentarios', 'valor', 'nota'
    ]
    show_change_link = True

    sortable = 'order'


@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    form = FormularioFormAdmin
    inlines = [TabelaAdminInline]
    raw_id_fields = ['atividade', 'sentenca_avulca']
    list_display = ['titulo', 'atividade', 'sentenca_avulca']
    list_filter = ['atividade', 'sentenca_avulca']
    search_fields = ['titulo', 'texto']

    def _copy(self, request, pk):
        formulario = Formulario.objects.get(pk=pk)
        formulario_cp = copy.copy(formulario)
        formulario_cp.id = None
        formulario_cp.atividade = None
        formulario_cp.sentenca_avulca = None
        formulario_cp.titulo = u'Cópia: {}'.format(formulario.titulo)
        formulario_cp.save()

        # Add tabelas
        for tabela in formulario.tabelas.all():
            tbl = copy.copy(tabela)
            tbl.id = None
            tbl.formulario = formulario_cp
            # tbl.nota.clear()
            tbl.save()
            for nota in tabela.nota.all():
                tbl.nota.add(nota)
            tbl.save()

        messages.success(request, u"{0}, Duplicado com sucesso.".format(formulario_cp))
        return redirect('/admin/formulario_correcao/formulario/%s/' % formulario_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(FormularioAdmin, self).response_change(request, obj)


@admin.register(Tabela)
class TabelaAdmin(SortableModelAdmin):
    list_per_page = 50
    form = TabelaFormAdmin
    # fieldsets = [
    #     ("Geral", {
    #         'classes': ('suit-tab', 'suit-tab-general',),
    #         'fields': ['formulario', 'item', 'valor', 'proibir_negativa', 'comentarios']
    #     }),
    #     ('Notas', {
    #         'classes': ('suit-tab', 'suit-tab-notas',),
    #         'fields': ['nota']}),
    # ]
    # suit_form_tabs = (('general', 'Geral'), ('notas', 'Notas'))
    # suit_form_includes = (
    #     ('formulario_corecao/admin/notas.html', 'top', 'notas'),
    # )
    list_display = [
        'item', 'formulario', 'valor'
    ]
    list_filter = [
        ('formulario', admin.RelatedOnlyFieldListFilter)
    ]
    search_fields = ['item', 'formulario__titulo']
    raw_id_fields = ['nota']

    sortable = 'order'

    def response_change(self, request, obj):
        response = super(TabelaAdmin, self).response_change(request, obj)
        if request.POST.get("_send_back"):
            response = redirect('/admin/formulario_correcao/formulario/%s/' % obj.formulario.id)
        return response

    def get_queryset(self, request):
        qs = super(TabelaAdmin, self).get_queryset(request)
        return qs.prefetch_related("nota")

@admin.register(TabelaAluno)
class TabelaAlunoAdmin(admin.ModelAdmin):
    form = FormularioFormAdmin
    raw_id_fields = ['notas']
    # list_filter = [
    #     ('tabela_correcao', admin.RelatedOnlyFieldListFilter)
    # ]
    list_display = ['tabela_correcao', 'tabela', 'nota']


class TabelaAlunoInline(admin.TabularInline):
    filter_horizontal = ['notas']
    model = TabelaAluno
    fields = ['notas', 'nota']
    extra = 0


def make_paid(modeladmin, request, queryset):
    queryset.update(pago=True)
    messages.success(request, u"{} Registro(s) marcado(s) como pago.".format(queryset.count()))


make_paid.short_description = "Marcar como pago"


@admin.register(TabelaCorrecaoAluno)
class TabelaCorrecaoAlunoAdmin(admin.ModelAdmin):
    # inlines = [TabelaAlunoInline]
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()}
    }
    list_filter = [
        ('aluno', admin.RelatedOnlyFieldListFilter),
        ('professor', admin.RelatedOnlyFieldListFilter),
        ('formulario', admin.RelatedOnlyFieldListFilter),
        'formulario__sentenca_avulca__curso__categoria__tipo',
        'corrigido',
        'pago',
        'data_correcao'
    ]
    search_fields = [
        'aluno__nome', 'formulario__titulo', 'texto'
    ]
    list_display = [
        'aluno',
        'formulario',
        'corrigido',
        'data_correcao',
        'professor',
        'pago'
    ]
    actions = [make_paid]
