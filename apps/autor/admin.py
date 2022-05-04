# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.text import mark_safe
from django_localflavor_br.forms import BRCNPJField, BRCPFField
from nested_admin.nested import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from suit.admin import SortableStackedInline
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Autor,
    Banco,
    AssuntoGeral,
    AssuntoEspecifico,
    QuestaoC,
    QuestaoM,
    Questao,
    QuestaoEscolha,
    Simulado,
    GrupoSimulado,
    GrupoDoSimulado,
    DisciplinaGrupo,
    QuestaoGrupo,
    DisciplinaConcurso,
    QuestionarioAluno,
    RespostaQuestionarioAluno,
    Resultado,
    ResultadoResposta
)

_ck_editor_toolbar = [
    {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
    {'name': 'paragraph',
     'groups': ['list', 'indent', 'blocks', 'align']},
    {'name': 'styles'}, {'name': 'colors'},
    {'name': 'insert_custom',
     'items': ['Image', 'Flash', 'Table', 'HorizontalRule']}
]

_ck_editor_config = {'autoGrow_onStartup': True,
                     'autoGrow_minHeight': 100,
                     'autoGrow_maxHeight': 250,
                     'extraPlugins': 'autogrow',
                     'toolbarGroups': _ck_editor_toolbar}


class AutorForm(forms.ModelForm):
    cpf = BRCPFField(label='CPF')
    cnpj = BRCNPJField(label='CNPJ', required=False)

    class Meta:
        fields = '__all__'
        model = Autor


class BancoInLine(admin.StackedInline):
    model = Banco
    extra = 0
    suit_classes = 'suit-tab suit-tab-banco'


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    form = AutorForm
    inlines = [BancoInLine]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['user', 'nome', ('cpf', 'rg'), 'data_nascimento', 'pis', 'email', ('ddd_telefone', 'telefone'),
                       ('ddd_celular', 'celular')]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-endereco'),
            'fields': ['cep', 'logradouro', 'numero', 'bairro', 'complemento', ('cidade', 'uf')]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-banco'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-recebimentos'),
            'fields': ['tipo_recebimento', 'cnpj', 'endereco']
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('endereco', 'Endereço'),
        ('banco', 'Banco'),
        ('recebimentos', 'Recebimento'),
    )

    list_display = ('nome', 'email', 'user', 'cpf')
    list_filter = ('user', 'email', 'cpf')
    search_fields = ['nome']


@admin.register(AssuntoGeral)
class AssuntoGeralAdmin(admin.ModelAdmin):
    list_display = ['nome', 'disciplina']
    list_filter = ['disciplina']
    search_fields = ['nome']
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 80%'})}
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        pass

    def _copy(self, request, pk):
        assunto = AssuntoGeral.objects.get(pk=pk)
        assunto_cp = copy.copy(assunto)
        assunto_cp.id = None
        assunto_cp.nome = u'{} - Cópia'.format(assunto.nome)
        assunto_cp.disciplina = assunto.disciplina
        assunto_cp.save()

        messages.success(request, u"Assunto Geral [{}], Duplicada com sucesso.".format(assunto.nome))
        return redirect('/admin/autor/assuntogeral/%d/' % assunto_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(AssuntoGeralAdmin, self).response_change(request, obj)

    def response_post_save_add(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(AssuntoGeralAdmin, self).response_post_save_add(request, obj)


@admin.register(AssuntoEspecifico)
class AssuntoEspecificoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'disciplina', 'assunto_geral']
    search_fields = ['nome']
    list_filter = ['disciplina', 'assunto_geral']
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 80%'})}
    }

    def _copy(self, request, pk):
        assunto = AssuntoEspecifico.objects.get(pk=pk)
        assunto_cp = copy.copy(assunto)
        assunto_cp.id = None
        assunto_cp.nome = u'{} - Cópia'.format(assunto.nome)
        assunto_cp.disciplina = assunto.disciplina
        assunto_cp.assunto_geral = assunto.assunto_geral
        assunto_cp.save()

        messages.success(request, u"Assunto Especifico [{}], Duplicada com sucesso.".format(assunto.nome))
        return redirect('/admin/autor/assuntoespecifico/%d/' % assunto_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(AssuntoEspecificoAdmin, self).response_change(request, obj)

    def response_post_save_add(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(AssuntoEspecificoAdmin, self).response_post_save_add(request, obj)


class EscolhaFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super(EscolhaFormSet, self).clean()
        if not len(self.forms):
            pass
        elif len(self.forms) >= 2:
            count = 0
            self.forms[0].valid = False
            for form in self.forms:
                data = form.cleaned_data
                count += 1 if data.get('correta') else 0
                if count > 1:
                    form.add_error('correta', 'Escolha uma opção')
            if not count:
                form.add_error('correta', 'Escolha uma opção')
                raise ValidationError('Informe a opção correta!')

            if count > 1:
                raise ValidationError('Somente uma opção pode estar correta!')
        else:
            self.add_error('correta', 'Escolha uma opção')
            raise ValidationError('Informe no mínimo 2 alternativas.')


class QuestaoEscolhaInline(SortableStackedInline):
    model = QuestaoEscolha
    formset = EscolhaFormSet
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='custom-toolbar')},
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 80%'})}
    }
    suit_classes = 'suit-tab suit-tab-multipla'
    min_num = 0
    extra = 0
    sortable = 'order'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.situacao != 'E' and not request.user.is_superuser:
                self.can_delete = False
                fields = ['correta', 'texto', 'comentario_str']
                self.fields = fields
                return fields
        return self.readonly_fields

    def comentario_str(self, obj):
        return mark_safe(obj.comentario)

    comentario_str.short_description = 'Comentário'


def make_paid(modeladmin, request, queryset):
    queryset.update(situacao_financeira='A', data_pagamento=timezone.now())


make_paid.short_description = "Alterar para Pago"


def utilizada(obj):
    count = len(obj.get_simulados())
    css = 'error' if not count else 'success'
    return mark_safe('<strong class="text-%s">%dx</strong>' % (css, count))


class QuestaoUtilizadaFilter(admin.SimpleListFilter):
    title = 'Questões usadas'
    parameter_name = 'usadas'

    def lookups(self, request, model_admin):
        return [
            ('sim', 'Sim'),
            ('nao', 'Não'),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == 'sim':
            # Get websites that have at least one page.
            return queryset.filter(questoes_grupo__disciplina_grupo__grupo_simulado__isnull=False).distinct()
        else:
            # Get websites that don't have any pages.
            return queryset.filter(questoes_grupo__disciplina_grupo__grupo_simulado__isnull=True).distinct()


def simulados_str(obj):
    return ','.join(map(lambda x: x.nome, obj.simulados()))


simulados_str.short_description = 'Simulados'
utilizada.short_description = 'Utilizada'


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    inlines = [QuestaoEscolhaInline]
    tipoq = None
    raw_id_fields = [
        'user'
    ]
    list_display = [
        'tipo',
        'codigo',
        utilizada,
        'autor',
        'disciplina',
        'nivel',
        'data_criacao',
        'situacao_financeira',
        'situacao',
        'opcoes'
    ]

    list_filter = [
        'tipo',
        'disciplina',
        ('assunto_geral', admin.RelatedOnlyFieldListFilter),
        'assunto_especifico',
        'situacao',
        'situacao_financeira',
        'nivel',
        'autor',
        QuestaoUtilizadaFilter
    ]

    list_display_links = [
        'codigo'
    ]

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='custom-toolbar')},
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 80%'})},
    }

    readonly_fields = [
        'codigo',
        'data_criacao',
        'autor',
        'situacao',
        'situacao_financeira',
        'data_pagamento',
        'user',
        'autor',
        'situacao_financeira',
        'situacao',
    ]

    actions = [
        make_paid
    ]

    suit_form_includes = (
        ('autor/admin/questao-info.html', 'top', 'info')
    )

    def get_fieldsets(self, request, obj=None):
        if self.model._meta.model_name == 'questaoc':
            suit_form_tabs = [
                ('geral', 'Geral'),
                ('enunciado', 'Enunciado'),
                ('info', 'Informações')
            ]

            fieldsets = [(
                None, {
                    'classes': ('suit-tab', 'suit-tab-geral'),
                    'fields': ['nivel', 'disciplina', 'assunto_geral', 'assunto_especifico']
                }), (
                None, {
                    'classes': ('suit-tab', 'suit-tab-enunciado'),
                    'fields': ['correta', 'enunciado', 'comentario']
                }), (
                None, {
                    'classes': ('suit-tab', 'suit-tab-info'),
                    'fields': ['codigo', 'data_criacao', 'user', 'autor', 'situacao', 'situacao_financeira',
                               'data_pagamento']
                }),
            ]
        else:
            suit_form_tabs = [
                ('geral', 'Geral'),
                ('enunciado', 'Enunciado'),
                ('multipla', 'Escolhas'),
                ('info', 'Informações')
            ]

            fieldsets = [(
                None, {
                    'classes': ('suit-tab', 'suit-tab-geral'),
                    'fields': ['nivel', 'disciplina', 'assunto_geral', 'assunto_especifico']
                }), (
                None, {
                    'classes': ('suit-tab', 'suit-tab-enunciado'),
                    'fields': ['enunciado']
                }), (
                None, {
                    'classes': ('suit-tab', 'suit-tab-multipla'),
                    'fields': []
                }), (
                None, {
                    'classes': ('suit-tab', 'suit-tab-info'),
                    'fields': ['codigo', 'data_criacao', 'user', 'autor', 'situacao', 'situacao_financeira',
                               'data_pagamento']
                }),
            ]

        self.suit_form_tabs = suit_form_tabs

        return fieldsets

    def suit_row_attributes(self, obj, request):
        css_class = {
            'E': 'info',
            'A': 'warning',
            'H': 'success',
            'D': 'error',
        }.get(obj.situacao)
        if css_class:
            return {'class': css_class, 'data': obj.situacao}

    def save_model(self, request, obj, form, change):
        print('SAVE ADMIN')
        user = request.user
        q = Questao.objects.filter(id__isnull=False).last()
        if not q:
            pki = 1
        else:
            if q.pk:
                pki = q.pk + 1
            else:
                pki = q.pk

        # if self.model._meta.model_name == 'questaoc':
        #     tipo = 'C'
        # else:
        #     tipo = 'M'
        if not change:
            obj.tipo = self.tipoq
            obj.user = user
            try:
                obj.autor = user.autor
            except Autor.DoesNotExist:
                self.message_user(request, 'Usuário não existe para o Autor "{}"'.format(user), messages.WARNING)

            obj.pk = pki
            obj.codigo = '{}{:07d}'.format(self.tipoq, pki)

        super(QuestaoAdmin, self).save_model(request, obj, form, change)
        if self.tipoq == 'C':
            correta = obj.correta

            try:
                qc = QuestaoEscolha.objects.get(tipo='C', questao=obj)
                qc.correta = correta
            except QuestaoEscolha.DoesNotExist:
                qc = QuestaoEscolha(
                    questao_id=obj.id,
                    tipo='C',
                    order=0,
                    texto='Correta',
                    comentario=obj.comentario,
                    correta=correta
                )
            qc.save()

            try:
                qe = QuestaoEscolha.objects.get(tipo='E', questao=obj)
                qe.correta = False if correta else True
            except QuestaoEscolha.DoesNotExist:
                qe = QuestaoEscolha(
                    questao_id=obj.id,
                    tipo='E',
                    order=1,
                    texto='Errada',
                    comentario=obj.comentario,
                    correta=False if correta else True
                )
            qe.save()

    def get_queryset(self, request):
        qs = super(QuestaoAdmin, self).get_queryset(request=request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    def get_actions(self, request):
        actions = super(QuestaoAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            if 'make_paid' in actions:
                del actions['make_paid']
        return actions

    def get_list_filter(self, request):
        if not request.user.is_superuser:
            return ['situacao', 'situacao_financeira', 'nivel']
        return self.list_filter

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['codigo', 'data_criacao', 'user']
        if obj:
            if obj.situacao != 'E':
                return Questao._meta.get_all_field_names()
        return self.readonly_fields

    def response_change(self, request, obj):
        if "_send_approve" in request.POST:
            msg_tag = messages.SUCCESS
            try:
                obj.situacao = 'A'
                obj.save()
                msg = 'A Questão "{}" foi enviada para aprovação'.format(obj)
            except Exception as e:
                msg_tag = messages.ERROR
                msg = str(e)

            self.message_user(request, msg, msg_tag)
        return super(QuestaoAdmin, self).response_change(request, obj)


@admin.register(QuestaoC)
class QuestaoCAdmin(QuestaoAdmin):
    tipoq = 'C'
    list_filter = [
        'disciplina',
        'assunto_geral',
        'assunto_especifico',
        'situacao',
        'situacao_financeira',
        'nivel',
        'autor',
    ]
    list_display_links = ['codigo', 'autor']

    readonly_fields = ['codigo', 'data_criacao']


@admin.register(QuestaoM)
class QuestaoAdminM(QuestaoAdmin):
    tipoq = 'M'

    def get_queryset(self, request):
        qs = super(QuestaoAdminM, self).get_queryset(request=request)
        if not request.user.is_superuser:
            qs.filter(user=request.user, tipo='M')
        return qs


class QuestaoGrupoInline(NestedTabularInline):
    model = QuestaoGrupo
    extra = 0
    fk_name = 'disciplina_grupo'
    raw_id_fields = ['questao']


class DisciplinaGrupoInline(NestedStackedInline):
    model = DisciplinaGrupo
    extra = 0
    fk_name = 'grupo_simulado'
    inlines = [QuestaoGrupoInline]


@admin.register(QuestaoGrupo)
class QuestaoGrupoAdmin(admin.ModelAdmin):
    list_display = [
        'numeracao', 'questao', 'disciplina_grupo'
    ]
    list_display_links = [
        'numeracao', 'questao'
    ]
    list_filter = [
        ('questao', admin.RelatedOnlyFieldListFilter),
        ('disciplina_grupo', admin.RelatedOnlyFieldListFilter)
    ]


@admin.register(GrupoSimulado)
class GrupoSimuladoAdmin(NestedModelAdmin):
    inlines = [DisciplinaGrupoInline]
    list_filter = ['active']

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "active__exact=1"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(GrupoSimuladoAdmin, self).changelist_view(request, extra_context=extra_context)


class GrupoSimuladoInLineAdmin(admin.TabularInline):
    model = GrupoDoSimulado
    fk_name = 'simulado'
    extra = 0


@admin.register(Simulado)
class SimuladoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'esfera_geral',
                    'esfera_especifica',
                    'cargo', 'area_profissional',
                    'concurso', 'data_prova']
    search_fields = ['nome']
    inlines = [GrupoSimuladoInLineAdmin]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='custom-toolbar')},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget()}
    }

    def suit_row_attributes(self, obj, request):
        css_class = {
            'C': 'info',
            'M': 'success'
        }.get(obj.tipo)
        if css_class:
            return {'class': css_class, 'data': obj.tipo}

    def _copy(self, request, pk):
        simulado = Simulado.objects.get(pk=pk)
        simulado_cp = copy.copy(simulado)

        simulado_cp.id = None
        simulado_cp.nome = '[COPIA] %s' % simulado.nome
        simulado_cp.area_profissional_id = None
        simulado_cp.concurso = None
        simulado_cp.cargo = None
        simulado_cp.save()

        messages.success(request, u"Simulado {}, Duplicado com sucesso.".format(simulado_cp.pk))
        return redirect('/admin/autor/simulado/%d/' % simulado_cp.pk)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(SimuladoAdmin, self).response_change(request, obj)


@admin.register(DisciplinaGrupo)
class DisciplinaGrupoAdmin(admin.ModelAdmin):
    inlines = [
        QuestaoGrupoInline
    ]
    list_display = [
        'disciplina', 'peso', 'nota_minima', 'grupo_simulado'
    ]
    list_filter = [
        ('disciplina', admin.RelatedOnlyFieldListFilter),
        ('grupo_simulado', admin.RelatedOnlyFieldListFilter)
    ]


@admin.register(QuestaoEscolha)
class QuestaoEscolhaAdmin(admin.ModelAdmin):
    list_filter = [
        'questao',
        'questao__tipo'
    ]
    list_display = [
        'questao',
        'correta',
        'order'
    ]



@admin.register(DisciplinaConcurso)
class DisciplinaConcursoAdmin(admin.ModelAdmin):
    filter_horizontal = ['disciplinas']


search_fields = [
    'aluno',
    'simulado'
]


@admin.register(RespostaQuestionarioAluno)
class RespostaQuestionarioAlunoAdmin(admin.ModelAdmin):
    list_filter = [
        ('questionario_aluno', admin.RelatedOnlyFieldListFilter),
        'correta'
    ]
    list_display = [
        'questionario_aluno',
        'questao_escolha',
        'questao_grupo',
        'correta',
        'respondida',
        'data_criacao'
    ]
    raw_id_fields = [
        'questao_escolha'
    ]


@admin.register(QuestionarioAluno)
class QuestionarioAlunoAdmin(admin.ModelAdmin):
    list_display = [
        'aluno',
        'simulado',
        'data_criacao',
        'data_conclusao',
        'pontuacao',
        'simulado_status',
        'aprovado'
    ]
    list_filter = [
        ('aluno', admin.RelatedOnlyFieldListFilter),
        ('simulado', admin.RelatedOnlyFieldListFilter),
        'data_criacao',
        'data_conclusao',
    ]

    def simulado_status(self, obj):
        return obj.simulado.situacao_desc.get('title')

    simulado_status.short_description = 'Status Simulado'

    def suit_row_attributes(self, obj, request):
        css_class = {
            'success': 'success',
            'info': 'info',
            'danger': 'error'
        }.get(obj.simulado.situacao_desc.get('tag'))
        if css_class:
            return {'class': css_class, 'data': obj.simulado.pk}


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    pass


@admin.register(ResultadoResposta)
class ResultadoRespostaAdmin(admin.ModelAdmin):
    pass
