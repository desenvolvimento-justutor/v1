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
    list_display = ['titulo', 'valor']
    search_fields = ['texto', 'titulo']

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
        'item', 'valor',  #, 'comentarios', 'valor', 'nota'
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
    form = TabelaFormAdmin
    list_display = [
        'item', 'formulario', 'valor'
    ]
    list_filter = [
        ('formulario', admin.RelatedOnlyFieldListFilter)
    ]
    search_fields = ['item', 'formulario__titulo']
    filter_horizontal = ['nota']

    sortable = 'order'

    def response_change(self, request, obj):
        response = super(TabelaAdmin, self).response_change(request, obj)
        if request.POST.get("_send_back"):
            response = redirect('/admin/formulario_correcao/formulario/%s/' % obj.formulario.id)
        return response

@admin.register(TabelaAluno)
class TabelaAlunoAdmin(admin.ModelAdmin):
    form = FormularioFormAdmin
    filter_horizontal = ['notas']
    list_filter = [
        'tabela_correcao', 'tabela'
    ]
    list_display = ['tabela_correcao', 'tabela', 'nota']


class TabelaAlunoInline(admin.TabularInline):
    filter_horizontal = ['notas']
    model = TabelaAluno
    fields = ['notas', 'nota']
    extra = 0


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
        'corrigido'
    ]
    search_fields = [
        'aluno__nome', 'formulario__titulo', 'texto'
    ]
    list_display = [
        'aluno',
        'formulario',
        'corrigido',
        'professor'
    ]
