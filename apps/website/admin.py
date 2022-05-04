# -*- coding: utf-8 -*-
# Autor: christian
from django.contrib import admin
from django.forms import ModelForm
from mptt.admin import MPTTModelAdmin
from redactor.widgets import RedactorEditor
from sorl.thumbnail.admin import AdminImageMixin
from suit.admin import SortableModelAdmin
from suit.admin import SortableStackedInline
from suit.widgets import SuitSplitDateTimeWidget, EnclosedInput, AutosizedTextarea, HTML5Input, TextInput, Textarea

from .models import (Institucional, Banner, Configuracao, Endereco, Imagem, Noticia, VideoJusTutor, Anuncio,
                     ArtigoIndice, Artigo, PacoteDesconto)

toolbar_Full = [
    {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']},
    {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
    {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
    {'name': 'forms', 'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                                'HiddenField']},
    '/',
    {'name': 'basicstyles',
     'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
    {'name': 'paragraph',
     'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
               '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']},
    {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
    {'name': 'insert',
     'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
    '/',
    {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
    {'name': 'colors', 'items': ['TextColor', 'BGColor']},
    {'name': 'tools', 'items': ['Maximize', 'ShowBlocks', '-', 'About']}
]

_TB_BASIC = [
    {'name': 'document', 'items': ['Source', '-', 'NewPage', 'Preview']},
    {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
    {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll', '-', 'Scayt']},
    {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
    '/',
    {'name': 'styles', 'items': ['Styles', 'Format']},
    {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Strike', '-', 'RemoveFormat']},
    {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']},
    {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
    {'name': 'tools', 'items': ['Maximize', '-', 'About']}
]


class MetaFieldsForm(ModelForm):
    class Meta:
        widgets = {
            'meta_description': EnclosedInput(prepend='icon-comment', attrs={'class': 'input-xxlarge'}),
            'meta_keywords': EnclosedInput(prepend='icon-tag', attrs={'class': 'input-xxlarge'}),
            'nota_rodape': RedactorEditor(),
            #'subs_texto': RedactorEditor(),
            'subs_bgcolor': HTML5Input(input_type='color'),
            'subs_buttonbgcolor': HTML5Input(input_type='color'),
            'subs_buttoncolor': HTML5Input(input_type='color'),
            'subs_closecolor': HTML5Input(input_type='color'),
            'subs_color': HTML5Input(input_type='color'),
            'subs_contentcolor': HTML5Input(input_type='color')
        }


class EnderecoInLine(admin.StackedInline):
    model = Endereco
    suit_classes = 'suit-tab suit-tab-endereco'
    extra = 0


class InstitucionalInLine(SortableStackedInline):
    model = Institucional
    suit_classes = 'suit-tab suit-tab-institucional'
    extra = 0


class ImagemInLine(AdminImageMixin, admin.TabularInline):
    model = Imagem
    suit_classes = 'suit-tab suit-tab-imagem'
    extra = 0


class PacoteDescontoInLine(admin.TabularInline):
    model = PacoteDesconto
    suit_classes = 'suit-tab suit-tab-descontos'
    extra = 0


class ConfiguracaoAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [ImagemInLine, PacoteDescontoInLine]
    form = MetaFieldsForm
    list_display = ('titulo', 'ativo')
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['ativo', 'titulo', 'logo', 'favicon', 'email', 'telefone']
        }),
        (None,
         {
             'classes': ('suit-tab suit-tab-endereco',),
             'fields': ['cep', 'endereco', 'numero', 'bairro', 'cidade', 'uf']
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-social',),
             'fields': ['url_facebook', 'url_flicker', 'url_twitter', 'url_youtube', 'url_instagram']
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-regulamento',),
             'fields': ['politica', 'termos', 'regulamento_premios', 'regulamento_sentenca_avulsa', 'sobre_drm']
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-seo ',),
             'fields': ['meta_description', 'meta_keywords', 'meta_geo_position', 'meta_geo_place',
                        'meta_geo_region']
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-imagem ',),
             'fields': []
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-newsletter ',),
             'fields': ['subs_ativo', 'subs_animacao', 'subs_posicao', 'subs_titulo', 'subs_texto', 'subs_texto_botao',
                        'subs_texto_sucesso', 'subs_texto_inferior', 'subs_imagem', 'subs_bgcolor',
                        'subs_buttonbgcolor', 'subs_buttoncolor', 'subs_closecolor', 'subs_color', 'subs_contentcolor'
                        ]
         }),
        (None,
         {
             'classes': ('suit-tab suit-tab-descontos',),
             'fields': []
         }),
    ]

    suit_form_tabs = (
        ('general', 'Geral'),
        ('endereco', 'Endereço'),
        ('regulamento', 'Regulamentos'),
        ('social', 'Redes Sociais'),
        ('seo', 'SEO'),
        ('imagem', 'Imagens'),
        ('newsletter', 'Newsletter'),
        ('descontos', 'Descontos'),
    )


class BannerFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'ativo_inicio': SuitSplitDateTimeWidget,
            'ativo_fim': SuitSplitDateTimeWidget,
        }


class BannerAdmin(AdminImageMixin, SortableModelAdmin):
    form = BannerFormAdmin
    sortable = 'order'
    list_display = (
        'titulo',
        'imagem',
        'ativo_inicio',
        'ativo_fim',
        'order'
    )
    list_editable = ('order',)
    fieldsets = (
        (None, {
            'fields': ('configuracao', 'exibir_caixa', 'titulo', 'legendas', 'imagem', 'link', 'texto_link')
        }),
        (None, {
            'fields': ('ativo_inicio', 'ativo_fim')
        }),
    )


class InstitucionalFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'conteudo': RedactorEditor(),
            'resumo': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'nome': TextInput(attrs={'class': 'input-xxlarge'}),
            'descricao': Textarea(attrs={'class': 'input-xxlarge'}),
        }

    class Media:
        js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        css = {
            'all': ('filebrowser/css/suit-filebrowser.css',)
        }


class InstitucionalAdmin(SortableModelAdmin):
    form = InstitucionalFormAdmin

    list_display = ('nome', 'url', 'configuracao', 'ativo', 'order')
    list_editable = ('order',)
    list_filter = ['ativo', 'configuracao__titulo']
    search_fields = ['nome']

    # Specify 'name' of sortable property
    sortable = 'order'


@admin.register(Noticia)
class NoticiaAdmin(AdminImageMixin, admin.ModelAdmin):
    form = InstitucionalFormAdmin

    list_display = ('nome', 'configuracao', 'ativo_inicio', 'ativo_fim')
    list_filter = ['ativo_inicio', 'configuracao__titulo']
    search_fields = ['nome']


class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_ini', 'video')


@admin.register(Anuncio)
class AnuncioAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('titulo', 'imagem_', 'pag_atividades', 'pag_cursos', 'pag_curso_gratis', 'pag_enunciados', 'pag_resultado_busca',
                    'pag_conteudo', 'pag_videos', 'pag_roteiro', 'pag_noticias', 'pag_temas', 'pag_populares', 'ativo')
    list_filter = ['pag_atividades', 'pag_cursos', 'pag_curso_gratis', 'pag_enunciados', 'pag_resultado_busca', 'pag_conteudo',
                   'pag_videos', 'pag_roteiro', 'pag_noticias', 'pag_temas', 'pag_populares']
    search_fields = ['titulo']


@admin.register(ArtigoIndice)
class ArtigoIndiceAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ['name']
    search_fields = ['name']


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    form = InstitucionalFormAdmin

    list_display = ('nome', 'indice', 'autor')
    list_filter = ['indice']
    search_fields = ['nome', 'autor']


admin.site.register(Institucional, InstitucionalAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(VideoJusTutor, VideoAdmin)
