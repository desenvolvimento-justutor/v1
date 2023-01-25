# -*- coding: utf-8 -*-
# Autor: christian
from __future__ import unicode_literals

import copy
import csv

from django.contrib import admin
from django.contrib import messages
from django.db import models
from django.forms import ModelForm, TextInput, Select, ModelChoiceField
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.text import slugify
from redactor.widgets import RedactorEditor
from sorl.thumbnail.admin import AdminImageMixin
from suit.admin import SortableModelAdmin, SortableTabularInline
from suit.widgets import AutosizedTextarea, SuitSplitDateTimeWidget, EnclosedInput, SuitDateWidget, LinkedSelect
from suit_ckeditor.widgets import CKEditorWidget

from apps.cupom.models import Cupom
from models import (Categoria, Curso, Destaque, Modulo, VideoModulo, PdfModulo, Serie, CursoGratis, VideoGratis,
                    DocCurso, CheckoutItens, Discussao, Atividade, TarefaAtividade, SentencaAvulsa, SentencaAvulsaAluno,
                    SentencaModelo, SentencaOAB, SentencaModeloOAB, SentencaOABAvulsaAluno, AtividadeModelo,
                    Certificado, Livro, Autor, Colecao, CursoCredito, Combo, ComboAluno, LiberarCompraCurso, Simulado,
                    Cortesia)


class CortesiaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CortesiaForm, self).__init__(*args, **kwargs)
        append = self.fields['codigo'].widget.append
        instance = kwargs.get('instance', False)
        if instance:
            self.fields['codigo'].widget.append = append.replace('datacopy', instance.codigo)

    class Meta:
        widgets = {
            # By icons
            'codigo': EnclosedInput(
                prepend='icon-tag',
                append='<button class="btn cpy" type="button" data-clipboard-text="datacopy" title="Copiar código">'
                       'Copiar'
                       '</button>',
                attrs={'readonly': 'readonly', 'class': 'span5'}),
        }


class CortesiaInLine(admin.TabularInline):
    model = Cortesia
    form = CortesiaForm
    extra = 0

    raw_id_fields = ['aluno']
    readonly_fields = ['utilizado']
    fields = [
        'codigo', 'aluno', 'email', 'utilizado'
    ]



@admin.register(CheckoutItens)
class CheckoutItensAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'curso'
    ]
    search_fields = [
        'curso__nome',
        'checkout__code',
        'checkout__aluno__nome'
    ]
    list_display = (
        'checkout',
        'curso'
    )
    list_filter = [
        ('curso', admin.RelatedOnlyFieldListFilter),
        ('checkout__aluno', admin.RelatedFieldListFilter)
    ]


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'chave')
    list_filter = ['aluno', 'curso']
    search_fields = list_display
    readonly_fields = ['chave']


@admin.register(Categoria)
class CategoriaAdmin(SortableModelAdmin):
    sortable = 'order'
    list_display = ('nome', 'order', 'tipo')
    list_filter = ['tipo']


class ModuloAdminInline(SortableTabularInline):
    model = Modulo
    extra = 0
    suit_classes = 'suit-tab suit-tab-modulos'
    sortable = 'order'


class DocCursoInline(SortableTabularInline):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget}
    }
    model = DocCurso
    extra = 0
    suit_classes = 'suit-tab suit-tab-material'


class DiscurssaoInline(admin.StackedInline):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget}
    }
    model = Discussao
    extra = 0
    suit_classes = 'suit-tab suit-tab-discussao'


class AtividadeForm(ModelForm):
    class Meta:
        widgets = {
            'enunciado': LinkedSelect
        }


class AtividadeInline(admin.StackedInline):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.TextField: {'widget': RedactorEditor()},
    }
    filter_horizontal = ['professores']
    model = Atividade
    extra = 0
    suit_classes = 'suit-tab suit-tab-atividade'


class CursoFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'descricao': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'}),
            'nome': TextInput(attrs={'class': 'span10'}),
            'data_ini': SuitSplitDateTimeWidget,
            'data_fim': SuitSplitDateTimeWidget,
            'valor': EnclosedInput(prepend='R$'),
            'economia': EnclosedInput(prepend='R$'),
            'parcelas': Select(attrs={'class': 'input-small'}),
            'tipo_duracao': Select(attrs={'class': 'input-small'}),
            'saiba_mais': RedactorEditor(),
            'cronograma': RedactorEditor(),
            'mural': RedactorEditor(),
            'certificado': CKEditorWidget(editor_options={'startupFocus': True})
        }



class LivroFormAdmin(ModelForm):
    class Meta:
        labels = {
            'imagem': 'Capa',
        }


@admin.register(Livro)
class LivroAdmin(SortableModelAdmin):
    filter_horizontal = ['autores']
    form = LivroFormAdmin
    list_display = ['nome', 'categoria', 'isbn', 'paginas', 'edicao', 'ano']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['categoria', 'colecao', 'nome', 'imagem', 'autores', 'valor', ('formato', 'paginas'), 'livro',
                       'amostra', 'sumario', 'descricao', ('edicao', 'ano'), 'isbn']
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(categoria__tipo='L')

    def response_change(self, request, obj):
        if request.POST.get("_lista_emails"):
            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="lista-{0}.csv"'.format(slugify(obj))

            writer = csv.writer(response)
            for aluno in obj.get_alunos:
                writer.writerow([aluno, aluno.email])
            return response

        return super(LivroAdmin, self).response_change(request, obj)


@admin.register(Combo)
class ComboAdmin(SortableModelAdmin):
    form = CursoFormAdmin
    filter_horizontal = ['cursos']
    list_display = ['nome', 'categoria']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['categoria', 'nome', 'descricao', 'imagem', 'data_ini', 'data_fim', ('valor', 'economia'),
                       'saiba_mais', 'cursos', 'slug']
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(categoria__tipo='B')


@admin.register(CursoCredito)
class CursoCreditoAdmin(SortableModelAdmin):
    form = CursoFormAdmin
    filter_horizontal = ['cursos']
    list_display = ['nome', 'categoria']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['categoria', 'nome', 'descricao', 'imagem', 'data_ini', 'data_fim', ('valor', 'economia'),
                       'saiba_mais', 'cursos', 'slug']
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(categoria__tipo='P')


@admin.register(ComboAluno)
class ComboAlunoAdmin(SortableModelAdmin):
    form = CursoFormAdmin
    filter_horizontal = ['cursos']
    list_filter = ['aluno', 'status']
    list_display = ['nome', 'aluno', 'status']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['aluno', 'status', 'categoria', 'nome', 'descricao', 'imagem', 'data_ini', 'data_fim',
                       ('valor', 'economia'), 'saiba_mais', 'cursos', 'slug']
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(categoria__tipo='B', aluno__isnull=False)


@admin.register(Autor)
class AutorAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    pass


class TarefaAtividadeForm(ModelForm):
    class Meta:
        widgets = {
            'tarefa': RedactorEditor(),
            'gabarito': RedactorEditor(),
            'descricao': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'})
        }


class TarefaAtividadeInLine(admin.StackedInline):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
    }
    form = TarefaAtividadeForm
    model = TarefaAtividade
    extra = 0


class AtividadeModeloAdmin(admin.TabularInline):
    model = AtividadeModelo


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
    }
    raw_id_fields = ['curso']
    form = TarefaAtividadeForm
    inlines = [AtividadeModeloAdmin]
    filter_horizontal = ['professores']
    list_display = ['nome', 'curso', 'data_ini', 'data_fim', 'tipo_retorno', 'resolucao_obrigatorio']
    list_filter = ['curso', 'tipo_retorno', 'resolucao_obrigatorio']
    search_fields = ['nome', 'curso__nome', 'tarefa', 'gabarito']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['curso', 'professores', 'tipo_retorno', 'nome', 'descricao', 'caracteres', 'data', 'data_ini', 'data_fim',
                       'resposta_padrao_data', 'resolucao_obrigatorio']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-tarefa'),
            'fields': ['tarefa']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-gabarito'),
            'fields': ['gabarito']
        })
    ]
    suit_form_tabs = [
        ('geral', 'Geral'),
        ('tarefa', 'Tarefa'),
        ('gabarito', 'Gabarito')
    ]

    def _copy(self, request, pk):
        atividade = Atividade.objects.get(pk=pk)
        atividade_cp = copy.copy(atividade)
        atividade_cp.id = None
        atividade_cp.data_ini = None
        atividade_cp.data_fim = None
        atividade_cp.resolucao_obrigatorio = None
        atividade_cp.curso = atividade.curso
        atividade_cp.nome = atividade.nome
        atividade_cp.descricao = atividade.descricao
        atividade_cp.gabarito = atividade.gabarito
        atividade_cp.tipo_retorno = atividade.tipo_retorno
        atividade_cp.tarefa = atividade.tarefa
        atividade_cp.resposta_padra = atividade.resposta_padra

        atividade_cp.save()
        # Add produtos
        for modelo in atividade.atividademodelo_set.all():
            modelo = AtividadeModelo(
                atividade=atividade_cp,
                arquivo=modelo.arquivo
            )
            modelo.save()

        messages.success(request, u"Atividade [{}], Duplicada com sucesso.".format(atividade_cp))
        return redirect('/admin/curso/atividade/%d/' % atividade_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(AtividadeAdmin, self).response_change(request, obj)


@admin.register(TarefaAtividade)
class TarefaAtividadeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()},
    }

    list_display = [
        'atividade',
        'aluno',
        'concluido',
        'tempo',
        'corrigido'
    ]

    list_filter = [
        'atividade__curso__categoria',
        'aluno',
        'concluido',
        'corrigido'
    ]

    search_fields = [
        'atividade__nome',
        'aluno__nome',
    ]

@admin.register(Cortesia)
class CortesiaAdmin(admin.ModelAdmin):
    list_display = ["curso", "codigo", "aluno", "utilizado"]

@admin.register(Curso)
class CursoAdmin(AdminImageMixin, SortableModelAdmin):
    actions = ['subscribe_aluno', 'gerar_cupons']

    list_per_page = 10

    form = CursoFormAdmin
    inlines = (ModuloAdminInline, DocCursoInline, DiscurssaoInline, AtividadeInline, CortesiaInLine)
    list_display = ('nome', 'categoria', 'valor', 'data_ini', 'data_fim', 'disponivel', 'matriculas', 'matriculados',
                    'is_video_curso', 'is_tutorial', 'order')
    list_editable = ('order',)
    list_filter = ('categoria', 'disponivel')
    search_fields = ['nome']
    filter_horizontal = ['professores', 'blocos']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['is_video_curso', 'is_tutorial', 'categoria', 'sentenca_avulsa', 'sentenca_oab', 'nome', 'descricao', 'valor', 'video',
                       'disponivel', 'inicio_gratis', 'imagem', 'thumbnail', 'data_ini', 'data_fim', 'blocos', 'slug',
                       'status']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-modulos'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-material'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-discussao'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-cronograma'),
            'fields': ['cronograma']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-mural'),
            'fields': ['mural']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-atividade'),
            'fields': ['limitar_correcao']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-professores'),
            'fields': ['professores']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ['saiba_mais']}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-certificado', 'full-width'),
            'fields': ['certificado_data_ini', 'certificado']}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-cortesia'),
            'fields': []
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('modulos', 'Módulos'),
        ('seo', 'Saiba+'),
        ('material', 'Material'),
        ('discussao', 'Discussão'),
        ('cronograma', 'Cronograma'),
        ('mural', 'Mural'),
        ('atividade', 'Atividade'),
        ('professores', 'Professores'),
        ('certificado', 'Certificado'),
        ('cortesia', 'Cortesias'),
    )

    suit_form_includes = (
        ('curso/admin/var-info.html', 'top', 'certificado'),
        ('curso/admin/cortesia_info.html', 'top', 'cortesia'),
    )

    def subscribe_aluno(self, request, queryset):
        inc = 0
        total = 0
        for qs in queryset:
            chk = qs.checkoutitens_set.filter(
                checkout__transaction__status__in=['pago', 'disponivel']
            )
            inc += chk.count()
            for c in chk:
                aluno = c.checkout.aluno
                total += 1
                ret = aluno.subscribe()
                if ret:
                    inc += 1
        self.message_user(request, "{0} de {1} Aluno(s) foram inscritos no Newsletter.".format(inc, total))

    def gerar_cupons(self, request, queryset):
        cupom = Cupom.objects.create()
        for query in queryset:
            cupom.produtos.add(query)
        cupom.save()
        return redirect('/admin/cupom/cupom/%d/' % cupom.pk)

    subscribe_aluno.short_description = "Inscrever no Newsletter"

    def _copy(self, request, pk):
        curso = Curso.objects.get(pk=pk)
        curso_cp = copy.copy(curso)
        curso_cp.id = None
        curso_cp.categoria = curso.categoria
        curso_cp.limitar_correcao = 0
        curso_cp.sentenca_avulsa = None
        curso_cp.sentenca_oab = None
        curso_cp.sentenca_oab = None
        curso_cp.thumbnail = curso.thumbnail
        curso_cp.imagem = curso.imagem
        curso_cp.descricao = curso.descricao
        curso_cp.valor = curso.valor
        curso_cp.disponivel = curso.disponivel
        curso_cp.inicio_gratis = False
        curso_cp.data_ini = timezone.now()
        curso_cp.data_fim = None
        curso_cp.saiba_mais = curso.saiba_mais

        curso_cp.nome = u'{} - Cópia'.format(curso.nome)
        curso_cp.video = curso.video
        curso_cp.save()
        curso_cp.slug = "{0}-{1}".format(slugify(curso.nome), curso_cp.id)
        curso_cp.save()
        # Add professores
        for professor in curso.professores.all():
            curso_cp.professores.add(professor)
        # Duplicar Materiais
        for material in curso.doccurso_set.all():
            mt = copy.copy(material)
            mt.id = None
            mt.curso = curso_cp
            mt.titulo = material.titulo
            mt.file = material.file
            mt.data_ativo = timezone.now().date()
            mt.order = material.order
            mt.save()
        # Duplicar Modulos
        for modulo in curso.modulo_set.all():
            modulo_cp = copy.copy(modulo)
            modulo_cp.id = None
            modulo_cp.curso = curso_cp
            modulo_cp.save()
            for video in modulo.videomodulo_set.all():
                video_cp = copy.copy(video)
                video_cp.id = None
                video_cp.modulo = modulo_cp
                video_cp.save()
        # Duplicar Foruns
        for discus in curso.discussao_set.all():
            discus_x = copy.copy(discus)
            discus_x.id = None
            discus_x.curso = curso_cp
            discus_x.save()

        messages.success(request, u"{0}, Duplicado com sucesso.".format(curso_cp))
        return redirect('/admin/curso/curso/%s/' % curso_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_lista_emails"):
            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="lista-{0}.csv"'.format(slugify(obj))

            writer = csv.writer(response)
            for aluno in obj.get_alunos:
                writer.writerow([aluno, aluno.email])
            return response
        elif request.POST.get("_copy"):
            return self._copy(request, obj.id)

        return super(CursoAdmin, self).response_change(request, obj)

    # def get_queryset(self, request):
    #     return self.model.objects.exclude(categoria__tipo='L')


class SimuladoFormAdmin(ModelForm):
    categoria = ModelChoiceField(queryset=Categoria.objects.filter(tipo='D'))

    class Meta:
        model = Simulado
        fields = '__all__'

        widgets = {
            'descricao': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'}),
            'nome': TextInput(attrs={'class': 'span10'}),
            'data_ini': SuitSplitDateTimeWidget,
            'data_fim': SuitSplitDateTimeWidget,
            'valor': EnclosedInput(prepend='R$'),
            'economia': EnclosedInput(prepend='R$'),
            'parcelas': Select(attrs={'class': 'input-small'}),
            'tipo_duracao': Select(attrs={'class': 'input-small'}),
            'saiba_mais': RedactorEditor(),
            'certificado': CKEditorWidget(editor_options={'startupFocus': True})
        }


@admin.register(Simulado)
class SimuladoAdmin(AdminImageMixin, SortableModelAdmin):
    form = SimuladoFormAdmin
    inlines = (DocCursoInline, DiscurssaoInline, CortesiaInLine)
    list_display = ('nome', 'categoria', 'valor', 'data_ini', 'data_fim', 'disponivel', 'order')
    list_editable = ('order',)
    list_filter = ['disponivel']
    search_fields = ['nome']
    prepopulated_fields = {"slug": ("nome",)}

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['categoria', 'simulado', 'nome', 'descricao', 'valor', 'disponivel',
                       'inicio_gratis', 'imagem', 'thumbnail', 'data_ini', 'data_fim', 'slug']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': ['saiba_mais']}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-material'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-discussao'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-cortesia'),
            'fields': []
        }),
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('seo', 'Saiba+'),
        ('material', 'Material'),
        ('discussao', 'Discussão'),
        ('cortesia', 'Cortesias'),
    )
    suit_form_includes = (
        ('curso/admin/cortesia_info.html', 'top', 'cortesia'),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(categoria__tipo='D')

    def _copy(self, request, pk):
        simulado = Simulado.objects.get(pk=pk)
        simulado_cp = copy.copy(simulado)

        simulado_cp.id = None
        simulado_cp.simulado = None
        simulado_cp.nome = '[COPIA] %s' % simulado.nome
        simulado_cp.data_ini = None
        simulado_cp.data_fim = None
        simulado_cp.slug = slugify('[COPIA] %s' % simulado.nome)
        simulado_cp.save()
        # Duplicar Materiais
        for material in simulado.doccurso_set.all():
            mt = copy.copy(material)
            mt.id = None
            mt.curso = simulado_cp
            mt.save()
        # Duplicar Foruns
        for discus in simulado.discussao_set.all():
            discus_x = copy.copy(discus)
            discus_x.id = None
            discus_x.curso = simulado_cp
            discus_x.save()

        messages.success(request, u"Simulado {}, Duplicado com sucesso.".format(simulado_cp.pk))
        return redirect('/admin/curso/simulado/%d/' % simulado_cp.pk)

    def response_change(self, request, obj):
        if request.POST.get("_lista_emails"):
            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="lista-{0}.csv"'.format(slugify(obj))

            writer = csv.writer(response)

            chk = obj.checkoutitens_set.filter(
                checkout__transaction__status__in=['pago', 'disponivel']
            )
            alunos = []
            for c in chk:
                aluno = c.checkout.aluno
                if aluno not in alunos:
                    alunos.append(aluno)

            for aluno in alunos:
                writer.writerow([aluno, aluno.email])
            return response
        elif request.POST.get("_copy"):
            return self._copy(request, obj.id)

        return super(SimuladoAdmin, self).response_change(request, obj)


class VideoAdminInline(admin.TabularInline):
    model = VideoModulo
    extra = 0
    suit_classes = 'suit-tab suit-tab-videos'
    fields = ['titulo', 'thumbnail', 'descricao', 'tipo']


class PdfAdminInline(admin.TabularInline):
    model = PdfModulo
    extra = 0
    suit_classes = 'suit-tab suit-tab-pdf'


@admin.register(Modulo)
class ModuloAdmin(SortableModelAdmin):
    list_display = ('nome', 'curso')
    inlines = (VideoAdminInline, PdfAdminInline)
    list_filter = ('curso__nome',)
    search_fields = ['nome']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['curso', 'nome']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-videos'),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-pdf'),
            'fields': []
        })
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('videos', 'Videos'),
        ('pdf', 'Arquivos PDF')
    )


@admin.register(Destaque)
class DestaqueAdmin(SortableModelAdmin):
    list_display = ('curso', 'data_ini', 'data_fim', 'order')
    list_editable = ('order',)


@admin.register(VideoModulo)
class VideoModuloAdmin(admin.ModelAdmin):
    list_display = ('modulo', 'thumbnail', 'titulo', 'descricao')


@admin.register(Serie)
class SerirAdmin(SortableModelAdmin):
    sortable = 'order'
    list_display = ('nome', 'order')


class CursoGratisFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'descricao': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'}),
            'nome': TextInput(attrs={'class': 'span10'}),
        }


class VideoGratisFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'descricao': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'}),
            'titulo': TextInput(attrs={'class': 'span10'}),
            'data_ini': SuitSplitDateTimeWidget
        }


class VideoGratisAdminInline(AdminImageMixin, admin.StackedInline):
    form = VideoGratisFormAdmin
    model = VideoGratis
    extra = 0
    suit_classes = 'suit-tab suit-tab-videos'


@admin.register(CursoGratis)
class CursoGratisAdmin(SortableModelAdmin):
    form = CursoGratisFormAdmin
    inlines = [VideoGratisAdminInline]
    list_display = ('nome', 'serie', 'data_cadastro')
    list_filter = ('serie',)
    search_fields = ['nome']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-geral'),
            'fields': ['serie', 'nome', 'descricao', 'video', 'thumbnail']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-videos'),
            'fields': []
        })
    ]
    suit_form_tabs = (
        ('geral', 'Geral'),
        ('videos', u'Vídeos'),
    )


class SentencaModeloAdmin(admin.TabularInline):
    model = SentencaModelo


class SentencaModeloOABAdmin(admin.TabularInline):
    model = SentencaModeloOAB


@admin.register(SentencaAvulsa)
class SentencaAvulsaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()}
    }
    inlines = [SentencaModeloAdmin]

    list_display = ['titulo', 'esfera_especifica', 'tipo_procedimento', 'disciplina', 'nivel']
    list_filter = ['esfera_especifica', 'tipo_procedimento', 'disciplina', 'nivel']
    search_fields = ['titulo']

    def _copy(self, request, pk):
        sentenca = SentencaAvulsa.objects.get(pk=pk)
        sentenca_cp = copy.copy(sentenca)
        sentenca_cp.id = None
        sentenca_cp.titulo = u'{} - Cópia'.format(sentenca.titulo)
        sentenca_cp.cod_youtube = sentenca.cod_youtube
        sentenca_cp.esfera_especifica = sentenca.esfera_especifica
        sentenca_cp.tipo_procedimento = None
        sentenca_cp.disciplina = None
        sentenca_cp.nivel = sentenca.nivel
        sentenca_cp.professor = sentenca.professor
        sentenca_cp.amostra = sentenca.amostra
        sentenca_cp.conteudo = sentenca.conteudo
        sentenca_cp.comentario = sentenca.comentario
        sentenca_cp.save()

        messages.success(request, u"{0}, Duplicado com sucesso.".format(sentenca.titulo))
        return redirect('/admin/curso/sentencaavulsa/%s/' % sentenca_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(SentencaAvulsaAdmin, self).response_change(request, obj)


@admin.register(SentencaOAB)
class SentencaOABAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()}
    }
    inlines = [SentencaModeloOABAdmin]

    list_display = ['titulo', 'tipo_peca', 'disciplina', 'nivel']
    list_filter = ['tipo_peca', 'disciplina', 'nivel']


@admin.register(SentencaAvulsaAluno)
class SentencaAvulsaAlunoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()}
    }
    list_display_links = ['cod', 'sentenca_avulsa']
    list_display = ['cod', 'sentenca_avulsa', 'aluno', 'status']
    list_filter = ['sentenca_avulsa', 'aluno', 'status']
    search_fields = ['id', 'sentenca_avulsa__titulo', 'aluno__nome', 'resposta', 'correcao_individual']


@admin.register(SentencaOABAvulsaAluno)
class SentencaOABAvulsaAlunoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor()}
    }
    list_display_links = ['cod', 'sentenca_oab']
    list_display = ['cod', 'sentenca_oab', 'aluno', 'status']
    list_filter = ['sentenca_oab', 'aluno', 'status']


@admin.register(LiberarCompraCurso)
class LiberarCompraCursoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget}
    }
    list_display = ['codigo', 'aluno', 'curso', 'data', 'ativo']
    list_display_links = ['codigo', 'aluno']
    list_filter = ['curso']
    raw_id_fields = ['curso', 'aluno']
