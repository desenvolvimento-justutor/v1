# -*- coding: utf-8 -*-
import copy

from django.conf.urls import patterns
from django.contrib import admin
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from redactor.widgets import RedactorEditor
from sorl.thumbnail.admin import AdminImageMixin
from suit.admin import SortableStackedInline, SortableModelAdmin
from suit.widgets import AutosizedTextarea

from apps.website.utils import enviar_email
from .models import (EsferaGeral, EsferaEspecifica, Cargo, AreaProfissional, OrgaoEntidade, TipoProcedimento,
                     TipoPecaPratica, Disciplina, Tag, Concurso, EnunciadoPropostaSentenca, RankingPremiado,
                     EnunciadoPropostaPratica, EnunciadoPropostaDiscursiva, Resposta, NotaResposta,
                     RoteiroEstudoItem, RoteiroEstudoSubItem, TipoPecaSentenca, Organizador,
                     RoteiroEstudo, Localidade, EnunciadoProposta, Correcao, ComentarioCorrecao, RankingPremiadoRanking,
                     RankingPremiadoPremio, TagLinks, DisciplinaLinks)


class EsferaEspecificaInLine(admin.TabularInline):
    model = EsferaEspecifica
    extra = 0


@admin.register(EsferaGeral)
class EsferaGeralAdmin(admin.ModelAdmin):
    inlines = [EsferaEspecificaInLine]
    list_display = ['nome']
    search_fields = list_display


class CargoInLine(admin.TabularInline):
    model = Cargo
    extra = 0


@admin.register(EsferaEspecifica)
class EsferaEspecificaAdmin(admin.ModelAdmin):
    inlines = [CargoInLine]
    list_display = ['nome', 'esfera_geral']
    search_fields = ['nome']
    list_filter = ['esfera_geral']


# class EsferaEspecificaChoices(AutoModelSelect2Field):
#     queryset = EsferaEspecifica.objects
#     search_fields = ['nome__icontains', ]
#
#
# class CargoForm(ModelForm):
#     verbose_name = EsferaEspecifica._meta.verbose_name
#     esfera_especifica = EsferaEspecificaChoices(
#         label=verbose_name.capitalize(),
#         widget=AutoHeavySelect2Widget(
#             select2_options={
#                 'width': '220px',
#                 'placeholder': 'Buscar %s ...' % verbose_name
#             }
#         )
#     )

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'esfera_especifica']
    search_fields = ['nome']
    list_filter = ['esfera_especifica']
    # form = CargoForm


@admin.register(AreaProfissional)
class AreaProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = list_display


@admin.register(OrgaoEntidade)
class OrgaoEntidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(TipoProcedimento)
class TipoProcedimentoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(TipoPecaPratica)
class TipoPecaPraticaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(TipoPecaSentenca)
class TipoPecaSentencaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


class DisciplinaLinksInLine(admin.TabularInline):
    model = DisciplinaLinks
    extra = 0


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    inlines = [DisciplinaLinksInLine]
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cargo']
    search_fields = ['nome']
    list_filter = ['cargo']


@admin.register(Organizador)
class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Localidade)
class OrganizadorAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


class TagLinksInLine(admin.TabularInline):
    model = TagLinks
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TagLinksInLine]
    list_display = ['nome']
    search_fields = ['nome']


class ComumForm(ModelForm):
    class Meta:
        widgets = {
            'texto': RedactorEditor(),
            'ativo_motivo': RedactorEditor(),
            'excluir_motivo': RedactorEditor()
        }


# ---------------------------------------------
# ENUNCIADO/PROPOSTA - SENTENCA
# ---------------------------------------------
class EnunciadoPropostaSentencaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnunciadoPropostaSentencaForm, self).__init__(*args, **kwargs)
        # Defini os campos abaixo como requerido
        for field in EnunciadoPropostaSentenca.REQUIREDS:
            self.fields[field].required = True

    class Meta:
        widgets = {
            'texto': RedactorEditor(),
            'gabarito': RedactorEditor(),
            'audio': AutosizedTextarea(
                attrs={'class': 'span12'}
            )
        }


@admin.register(EnunciadoProposta)
class EnunciadoPropostaAdmin(admin.ModelAdmin):
    pass


@admin.register(EnunciadoPropostaSentenca)
class EnunciadoPropostaSentencaAdmin(admin.ModelAdmin):
    """
    Model admin para:
        <class 'apps.enunciado.models.EnunciadoPropostaPratica'>
    Proxy do Model:
        <class 'apps.enunciado.models.EnunciadoProposta'>
    """
    radio_fields = {'autor': admin.HORIZONTAL}
    form = EnunciadoPropostaSentencaForm
    list_display = EnunciadoPropostaSentenca.LIST_DISPLAY
    list_filter = EnunciadoPropostaSentenca.LIST_DISPLAY[1:]  # não exibir o titulo
    exclude = EnunciadoPropostaSentenca.EXCLUDE
    filter_horizontal = ['tags']
    search_fields = ['id', 'texto']

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'error',
        }.get(obj.desatualizado)
        if css_class:
            return {'class': css_class, 'data': obj.titulo}

    def get_queryset(self, request):
        return self.model.objects.filter(classificacao=EnunciadoPropostaSentenca.TIPO)

    def save_model(self, request, obj, form, change):
        obj.classificacao = EnunciadoPropostaSentenca.TIPO
        obj.save()

    def get_urls(self):
        urls = super(EnunciadoPropostaSentencaAdmin, self).get_urls()
        my_urls = patterns(
            '',
            (r'^(?P<pk>\d+)/copiar_enunciado/$', self.admin_site.admin_view(self.copiar_enunciado))
        )
        return my_urls + urls

    def copiar_enunciado(self, request, pk):
        enunciado = EnunciadoProposta.objects.get(pk=int(pk))
        enunciado_cp = copy.copy(enunciado)
        enunciado_cp.id = None
        enunciado_cp.disciplina = None
        enunciado_cp.texto = None
        enunciado_cp.save()
        messages.success(request, u"{0}, Criado com sucesso.".format(enunciado_cp))
        return redirect('/admin/enunciado/enunciadopropostasentenca/%s/' % enunciado_cp.id)

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.get("_copy"):
            return self.copiar_enunciado(request, obj.id)
        return super(EnunciadoPropostaSentencaAdmin, self).response_change(request, obj)


# ----------------------------------------------
# ENUNCIADO/PROPOSTA - PRATICA
# ---------------------------------------------
class EnunciadoPropostaPraticaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnunciadoPropostaPraticaForm, self).__init__(*args, **kwargs)

        # Defini os campos abaixo como requerido
        for field in EnunciadoPropostaPratica.REQUIREDS:
            self.fields[field].required = True

    class Meta:
        widgets = {
            'texto': RedactorEditor(),
            'audio': AutosizedTextarea(
                attrs={'class': 'span12'}
            )

        }


@admin.register(EnunciadoPropostaPratica)
class EnunciadoPropostaPraticaAdmin(admin.ModelAdmin):
    radio_fields = {'autor': admin.HORIZONTAL}
    form = EnunciadoPropostaPraticaForm
    list_display = EnunciadoPropostaPratica.LIST_DISPLAY
    list_filter = EnunciadoPropostaPratica.LIST_DISPLAY[1:]  # não exibir o titulo
    exclude = EnunciadoPropostaPratica.EXCLUDE
    filter_horizontal = ['tags']
    search_fields = ['id', 'texto']

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'error',
        }.get(obj.desatualizado)
        if css_class:
            return {'class': css_class, 'data': obj.titulo}

    def get_queryset(self, request):
        return self.model.objects.filter(classificacao=EnunciadoPropostaPratica.TIPO)

    def save_model(self, request, obj, form, change):
        obj.classificacao = EnunciadoPropostaPratica.TIPO
        obj.save()

    def get_urls(self):
        urls = super(EnunciadoPropostaPraticaAdmin, self).get_urls()
        my_urls = patterns(
            '',
            (r'^(?P<pk>\d+)/copiar_enunciado/$', self.admin_site.admin_view(self.copiar_enunciado))
        )
        return my_urls + urls

    def copiar_enunciado(self, request, pk):
        enunciado = EnunciadoProposta.objects.get(pk=int(pk))
        enunciado_cp = copy.copy(enunciado)
        enunciado_cp.id = None
        enunciado_cp.disciplina = None
        enunciado_cp.texto = None
        enunciado_cp.save()
        messages.success(request, u"{0}, Criado com sucesso.".format(enunciado_cp))
        return redirect('/admin/enunciado/enunciadopropostapratica/%s/' % enunciado_cp.id)

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.get("_copy"):
            return self.copiar_enunciado(request, obj.id)
        return super(EnunciadoPropostaPraticaAdmin, self).response_change(request, obj)


# ---------------------------------------------
# ENUNCIADO/PROPOSTA - DIRCURSIVA
# ---------------------------------------------
class EnunciadoPropostaDiscursivaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnunciadoPropostaDiscursivaForm, self).__init__(*args, **kwargs)

        # Defini os campos abaixo como requerido
        for field in EnunciadoPropostaDiscursiva.REQUIREDS:
            self.fields[field].required = True

    class Meta:
        widgets = {
            'texto': RedactorEditor(),
            'gabarito': RedactorEditor(),
            'audio': AutosizedTextarea(
                attrs={'class': 'span12'}
            )

        }


@admin.register(EnunciadoPropostaDiscursiva)
class EnunciadoPropostaDiscursivaAdmin(admin.ModelAdmin):
    radio_fields = {'autor': admin.HORIZONTAL}
    form = EnunciadoPropostaDiscursivaForm
    list_display = ['titulo', ] + EnunciadoPropostaDiscursiva.LIST_DISPLAY
    list_filter = EnunciadoPropostaDiscursiva.LIST_DISPLAY[1:]  # não exibir o titulo
    exclude = EnunciadoPropostaDiscursiva.EXCLUDE
    filter_horizontal = ['tags']
    search_fields = ['id', 'texto']

    # fieldsets = [
    #     ('Geral', {
    #         'classes': ('collapse',),
    #         'fields': [
    #             'esfera_geral', 'esfera_especifica', 'cargo', 'area_profissional',
    #             'orgao_entidade', 'concurso', 'data_prova', 'disciplina', 'num_questao_caderno',
    #             'organizador', 'localidade', 'desatualizado', 'tags']
    #     })
    # ]
    # suit_form_tabs = (
    #     ('enunciad', 'Enunciado'),
    # )

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'error',
        }.get(obj.desatualizado)
        if css_class:
            return {'class': css_class, 'data': obj.titulo}

    def get_queryset(self, request):
        return self.model.objects.filter(classificacao=EnunciadoPropostaDiscursiva.TIPO)

    def save_model(self, request, obj, form, change):
        obj.classificacao = EnunciadoPropostaDiscursiva.TIPO
        obj.save()

    def get_urls(self):
        urls = super(EnunciadoPropostaDiscursivaAdmin, self).get_urls()
        my_urls = patterns(
            '',
            (r'^(?P<pk>\d+)/copiar_enunciado/$', self.admin_site.admin_view(self.copiar_enunciado))
        )
        return my_urls + urls

    def copiar_enunciado(self, request, pk):
        enunciado = EnunciadoProposta.objects.get(pk=int(pk))
        enunciado_cp = copy.copy(enunciado)
        enunciado_cp.id = None
        enunciado_cp.disciplina = None
        enunciado_cp.num_questao_caderno = None
        enunciado_cp.texto = None
        enunciado_cp.save()
        messages.success(request, u"{0}, Criado com sucesso.".format(enunciado_cp))
        return redirect('/admin/enunciado/enunciadopropostadiscursiva/%s/' % enunciado_cp.id)

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.get("_copy"):
            return self.copiar_enunciado(request, obj.id)
        return super(EnunciadoPropostaDiscursivaAdmin, self).response_change(request, obj)


# ---------------------------------------------
# QUESTOES DOS ENUNCIADOS
# ---------------------------------------------
# @admin.register(Conteudo)
# class ConteudoAdmin(admin.ModelAdmin):
#     form = ComumForm
#
#     list_display = [
#         'titulo', 'enunciado', 'user', 'data'
#     ]
#     list_filter = [
#         'enunciado', 'user', 'data'
#     ]
#     search_fields = [
#         'id'
#     ]
#
#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         obj.save()


# ---------------------------------------------
# RESPOSTAS DAS QUESTOES
# ---------------------------------------------
class NotaRespostaInLine(admin.TabularInline):
    model = NotaResposta
    extra = 0
    suit_classes = 'suit-tab suit-tab-notas'


class CorrecaoInLine(admin.TabularInline):
    model = Correcao
    extra = 0
    form = ComumForm
    suit_classes = 'suit-tab suit-tab-correcao'


class ComentariosInLine(admin.TabularInline):
    model = ComentarioCorrecao
    extra = 0


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    form = ComumForm
    inlines = [
        NotaRespostaInLine, CorrecaoInLine
    ]

    list_display = [
        'enunciado', 'numero', 'aluno', 'data_inicio', 'data_termino', 'concluido'
    ]
    list_filter = [
        'aluno', 'enunciado', 'concluido', 'ativo'
    ]
    search_fields = [
        'id'
    ]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral',),
            'fields': ['aluno', 'enunciado', 'texto', ('tempo', 'concluido'), 'ativo', 'ativo_motivo']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-notas',),
            'fields': []}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-correcao',),
            'fields': []}),
    ]

    suit_form_tabs = (
        ('geral', 'Geral'), ('notas', 'Notas'), ('correcao', u'Correções'),
    )


@admin.register(Correcao)
class CorrecaoAdmin(admin.ModelAdmin):
    inlines = [ComentariosInLine]
    form = ComumForm
    list_display = [
        'aluno', 'resposta', 'data'
    ]
    list_filter = [
        'aluno', 'resposta'
    ]
    search_fields = [
        'id'
    ]

    def response_change(self, request, obj):
        if obj.excluir:
            enviar_email(
                'email/email-excluir-correcao.html', u'Correção excluída do site JusTutor',
                [obj.aluno.email], {'correcao': obj}, ead=True
            )
            obj.delete()
            messages.info(request, u'Correção excluída com sucesso.')
            return HttpResponseRedirect('/admin/enunciado/correcao/')
        else:
            return super(CorrecaoAdmin, self).response_change(request, obj)


class RoteiroEstudoSubItens(SortableStackedInline):
    model = RoteiroEstudoSubItem
    filter_horizontal = ['tags']
    extra = 0
    sortable = 'order'
    classes = ['collapse']


@admin.register(RoteiroEstudoItem)
class RoteiroEstudoItem(admin.ModelAdmin):
    inlines = [RoteiroEstudoSubItens]
    prepopulated_fields = {
        'slug': ['nome', 'roteiro']
    }
    list_display = ['nome', 'roteiro']
    list_filter = ['roteiro']


@admin.register(RoteiroEstudo)
class RoteiroEstudo(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['nome']
    }
    list_display = ['nome']


@admin.register(RoteiroEstudoSubItem)
class RoteiroEstudoSubItemAdmin(SortableModelAdmin):
    list_display = ['nome', 'item']
    list_filter = ['item']
    filter_horizontal = ['tags']
    sortable = 'order'


class RankingPremiadoPremioAdmin(AdminImageMixin, admin.TabularInline):
    model = RankingPremiadoPremio
    extra = 0


class RankingPremiadoRankingAdmin(admin.TabularInline):
    model = RankingPremiadoRanking
    extra = 0


@admin.register(RankingPremiado)
class RankingPremiadoAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [RankingPremiadoPremioAdmin]
    form = ComumForm
    list_display = [
        'nome', 'tipo_ranking', 'tipo_enunciado', 'data_ini', 'data_fim', 'encerrado'
    ]
    search_fields = [
        'nome'
    ]
    list_filter = [
        'tipo_ranking', 'tipo_enunciado', 'data_ini', 'data_fim', 'encerrado'
    ]
