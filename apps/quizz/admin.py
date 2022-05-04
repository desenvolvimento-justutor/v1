from django.contrib import admin
from .models import Bloco, Questao, Pergunta, Comentario, RespostaAluno
from redactor.widgets import RedactorEditor
from django.forms import ModelForm
from suit.widgets import AutosizedTextarea


class QuestaoFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'titulo': AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'}),
            'comentario': RedactorEditor(),
        }


class PerguntaFormAdmin(ModelForm):
    class Meta:
        widgets = {
            'titulo': AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'}),
        }


@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ['titulo']
    filter_horizontal = ['questoes']


class PerguntaInLine(admin.TabularInline):
    form = PerguntaFormAdmin
    model = Pergunta
    min_num = 2


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    inlines = [PerguntaInLine]
    search_fields = ['titulo']
    list_display = ['titulo']
    form = QuestaoFormAdmin


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['questao', 'aluno', 'comentario', 'data']


@admin.register(RespostaAluno)
class RespostaAlunoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'questao']
    list_filter = ['questao']
