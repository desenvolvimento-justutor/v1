import cStringIO as StringIO

from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from apps.enunciado.models import Resposta
from .models import Nota, RespostaAluno, Formulario


@csrf_exempt
def ajax_responder(request):
    aluno = request.user.aluno

    nota_pk = request.POST.get('notaPk')
    tabela_pk = request.POST.get('tabelaPk')
    nota = Nota.objects.get(pk=nota_pk)
    resposta_aluno, created = RespostaAluno.objects.update_or_create(
        aluno=aluno,
        tabela_id=tabela_pk,
        defaults={
            "nota": nota
        }
    )
    respostas = RespostaAluno.objects.filter(
        aluno=aluno,
        tabela__formulario=resposta_aluno.tabela.formulario,
        nota__isnull=False
    )
    notas = map(lambda x: x.nota.valor, respostas)
    vals = {
        'nota_pk': nota_pk,
        'tabela_pk': tabela_pk,
        'valor': nota.valor,
        'total': sum(notas),
    }
    print('post', nota_pk, tabela_pk, aluno.pk, resposta_aluno)

    return JsonResponse(vals)


def baixar_correcao(request, pk):
    print('***', request.GET)
    ctx = {}
    aluno = request.user.aluno
    formulario = get_object_or_404(Formulario, pk=pk)
    resposta = Resposta.objects.filter(
        aluno=aluno,
        enunciado=formulario.enunciado
    ).first()
    respostas = RespostaAluno.objects.filter(
        aluno=aluno,
        tabela__formulario=formulario,
        nota__isnull=False
    )
    notas = map(lambda x: x.nota.valor, respostas)
    ctx.update({
        'formulario': formulario,
        'aluno': aluno,
        'resposta': resposta,
        'total': sum(notas),
        'request': request,
        'action': request.GET.get('action', 'default'),
    })

    template = get_template('formulario_auto_correcao/baixar-correcao.html')
    context = Context(ctx)
    html = template.render(context)

    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % html)
