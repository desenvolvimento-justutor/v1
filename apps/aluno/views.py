# -*- coding: utf-8 -*-
# Autor: christian
import StringIO
import cStringIO as StringIO
import csv
import json
import re
import tempfile
from cgi import escape
from datetime import timedelta
from decimal import Decimal

import requests
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa

from apps.autor.models import QuestionarioAluno, Simulado
from apps.curso.models import (Atividade, Categoria, Certificado, CheckoutItens, Cortesia, Curso, Discussao,
                               SentencaAvulsaAluno, SentencaOABAvulsaAluno, TarefaAtividade, VideoModulo)
from apps.enunciado.models import Coletania, ComentarioCorrecao, Correcao, NotaResposta, NotificacoesAluno, Resposta
from apps.financeiro.models import ConfiguracaoPacote, Credito
from apps.formulario_auto_correcao.models import Formulario, RespostaAluno
from apps.formulario_correcao.models import Tabela, NotaCorrecao, TabelaCorrecaoAluno
from apps.formulario_correcao.templatetags.formulario_correcao_tags import soma_notas
from apps.professor.models import Mensagem as PMensagem
from carton.cart import Cart
from .forms import AlunoForm, CadastroAlunoForm
from .models import Aluno, Mensagem, Seguir, aluno_from_user_request
from django.template.loader import render_to_string


def split_name(name, last=False):
    name_split = name.split()
    if last and len(name_split) > 1:
        return ' '.join(name_split[1:])
    elif last and len(name_split) == 1:
        return ""
    return name_split[0]


@login_required
def perfil(request):
    context = {'filtro': {}}
    aluno = request.user.aluno

    if request.method == 'POST':
        data = request.POST
        dis = data.getlist('disciplinas')
        action = data.get('action')
        isprint = False
        if action == 'printcol':
            acao = data.get('acao')
            enunciado = data.get('enunciado')
            args = []

            if dis:
                args.append(Q(resposta__enunciado__disciplina__id__in=dis))
            if enunciado:
                args.append(Q(resposta__enunciado__classificacao=enunciado))
            context['filtro'] = {
                'disciplina': dis,
                'enunciado': enunciado,
            }
            resp = aluno.coletania_set.filter(*args)

            if acao == 'imprimir':
                isprint = True
                resp = map(lambda x: x.resposta, resp)
            else:
                context['coletaneas'] = resp
                context['tab'] = 'tab-coletanea'
        elif action == 'printresp':
            if dis:
                resp = aluno.resposta_set.filter(concluido=True, enunciado__disciplina__id__in=dis)
            else:
                resp = aluno.resposta_set.filter(concluido=True)
            isprint = True
        elif action == 'removercol':
            context['tab'] = 'tab-coletanea'
            col = Coletania.objects.get(id=request.POST.get('col_id'))
            col.delete()
            return HttpResponseRedirect(reverse('aluno:perfil') + '?tab=tab-coletanea')

        if isprint:
            ctx = dict(respostas=resp)
            template = get_template('imprimir-respostas.html')
            context2 = Context(ctx)
            html = template.render(context2)

            result = StringIO.StringIO()

            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        context['tab'] = request.GET.get('tab', 'tab-respostas')
        context['coletaneas'] = aluno.coletania_set.all()

    disciplinas = []
    for resposta in aluno.resposta_set.filter(ativo=True):
        disciplina = resposta.enunciado.disciplina
        if disciplina not in disciplinas:
            disciplinas.append(disciplina)

    disciplinas_col = []
    for col in aluno.coletania_set.all():
        disciplina = col.resposta.enunciado.disciplina
        if disciplina not in disciplinas_col:
            disciplinas_col.append(disciplina)

    context.update({
        'disciplinas_col': disciplinas_col,
        'disciplinas': disciplinas,
        'menu': 'perfil',
        'aluno': aluno,
        'transacoes': Correcao.objects.filter(aluno=aluno).order_by('-data'),
        'comentarios': ComentarioCorrecao.objects.filter(aluno=aluno).order_by('-data')
    })
    return render(request, 'painel-perfil.html', context)


@require_POST
@login_required
def relatorio(request):
    import re
    alunos = Aluno.objects.filter(
        cpf__isnull=False
    ).exclude(cpf='').order_by('nome')
    txt = u'================================================================================ =========== ======== ============================================================ ===== ========================= ========================= ====================================\r'
    txt += u'Nome                                                                             CPF         CEP      Logradouro                                                   No.   Bairro                    Cidade                    Email                         \r'
    txt += u'-------------------------------------------------------------------------------- ----------- -------- ------------------------------------------------------------ ----- ------------------------- ------------------------- ------------------------------------\r'

    for aluno in alunos:
        nm = aluno.nome
        if aluno.nome_completo:
            nm = u'{0} ({1})'.format(aluno.nome_completo, aluno.nome)
        cidade = ''
        if aluno.cidade:
            cidade = u'{0}-{1}'.format(aluno.cidade, aluno.uf)

        txt += u'{0:80} {1:11} {2:8} {3:60} {4:5} {5:25} {6:25} {7:36}\r'.format(
            nm.upper(),
            re.sub('[^0-9]', '', aluno.cpf),
            re.sub('[^0-9]', '', aluno.cep or ''),
            aluno.logradouro or '',
            aluno.numero or '',
            aluno.bairro or '',
            cidade.upper(),
            aluno.email
        )

    txt += u'================================================================================ =========== ======== ============================================================ ===== ========================= ========================= ====================================\r'
    txt += 'Total: {0}'.format(alunos.count())
    response = HttpResponse(txt, content_type='text/plain; charset=utf8')
    response['Content-Disposition'] = 'attachment; filename="lista-de-alunos.txt"'
    return response


@login_required
def livros(request):
    aluno = request.user.aluno
    cpf = aluno.cpf
    if not cpf:
        cpf = ''
    context = {
        'menu': 'Livros',
        'aluno': aluno,
        'senha': re.sub('[^0-9]', '', cpf)
    }
    checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])

    livros = []
    for c in checkouts:
        for livro in c.get_livros:
            livros.append(livro)
    context['meus_livros'] = livros
    context['checkouts'] = checkouts
    return render(request, 'painel-livros.html', context)


@login_required
def baixar_livro(request, lid):
    aluno = request.user.aluno
    aluno_pk = request.GET.get('aluno')
    if aluno_pk:
        aluno = Aluno.objects.get(id=aluno_pk)

    livro = get_object_or_404(Curso, pk=lid)
    if request.GET.get('action') == 'admin':
        rev = reverse("admin:admin-cursos-aluno", args=(aluno.pk,))
    else:
        rev = reverse('aluno:livros')
    if not aluno.cpf:
        messages.error(request, "Cadastre seu CPF para efetuar o Download")
        return HttpResponseRedirect(rev)
    if not aluno.email:
        messages.error(request, "Cadastre seu EMAIL para efetuar o Download")
        return HttpResponseRedirect(rev)

    if not aluno.email:
        messages.error(request, "Cadastre seu NOME para efetuar o Download")
        return HttpResponseRedirect(rev)

    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    # NOME ALUNO
    can.line(10, 42, 580, 42)
    can.setFont("Helvetica", 12)
    can.setFillColor('#000000')
    can.drawString(10, 30, u"{} ({})".format(aluno.nome, aluno.email))
    # COPYRIGHT
    can.setFont("Helvetica", 8)
    can.setFillColor('#D80017')
    can.drawString(10, 20, u"Esta obra foi adquirida pela pessoa acima identificada, sendo proibida a sua "
                           u"disponibilização para terceiros, a qualquer título e por qualquer meio, sob pena de ")
    can.drawString(10, 10, u"responsabilização cível e criminal")
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(livro.livro.path, strict=False)
    num_pages = existing_pdf.getNumPages()
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    for num in range(num_pages):
        page = existing_pdf.getPage(num)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
    # TEMP FILE
    tf = tempfile.NamedTemporaryFile()
    tf.close()
    senha = str(re.sub('[^0-9]', '', aluno.cpf))
    output.encrypt(senha, senha, use_128bit=True)
    # finally, write "output" to a real file
    outputStream = StringIO.StringIO()
    output.write(outputStream)
    # outputStream.close()
    # RESPONSE
    response = StreamingHttpResponse(outputStream.getvalue(), content_type='application/pdf; charset=utf8')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(slugify(livro.nome))
    return response


@login_required
def lista(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'
    alunos = Aluno.objects.filter(usuario__isnull=False).values('id', 'nome', 'email').order_by('id')
    fieldnames = [u'id', u'nome', u'email']
    writer = csv.writer(response, delimiter=';')

    writer.writerow(fieldnames)
    for aluno in alunos:
        writer.writerow([
            aluno['id'],
            aluno['nome'].encode('utf8'),
            aluno['email'].encode('utf8')
        ])

    return response


@login_required
def cursos(request, **kwargs):
    is_tutorial = kwargs.get("is_tutorial")
    aluno = request.user.aluno
    pagina = request.GET.get('videos', 'cursos')
    context = {
        'menu': 'Prática Dinâmica' if is_tutorial else 'cursos',
        'aluno': aluno,
        'pagina': pagina,
        'is_tutorial': is_tutorial
    }

    if request.method == 'POST':
        if request.POST.get('todos_cursos') == 'on':
            context['filtro'] = True
    else:
        request.session['videos'] = request.GET.get('videos')
        if request.user.is_superuser:
            context['filtro'] = True

    if pagina == 'cursos':
        request.session["url"] = "/aluno/cursos/?videos=%s" % pagina
        checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])
        context.update(dict(checkouts=checkouts))
    else:
        request.session["url"] = "/aluno/cursos/?videos=%s" % pagina
        checkout_item = get_object_or_404(CheckoutItens, id=pagina)
        trans = checkout_item.checkout.transaction
        if trans:
            if trans.status not in ['pago', 'disponivel']:
                messages.error(request, 'Transação pendente')
                raise PermissionDenied
            else:
                curso_id = request.GET.get('curso_id')
                if curso_id:
                    curso = Curso.objects.get(id=curso_id)
                else:
                    curso = checkout_item.curso
                request.session['curso_id'] = curso.pk

                alunos = checkout_item.curso.get_alunos
                modulos = curso.modulo_set.all().order_by('order')
                videos = VideoModulo.objects.filter(modulo__in=modulos)
                if aluno not in alunos:
                    messages.error(request, 'Você não participa deste curso')
                    raise PermissionDenied

                context.update(dict(
                    todas_msg=PMensagem.objects.filter(curso=curso, aluno=aluno),
                    msg_naolidas=PMensagem.objects.filter(curso=curso, aluno=aluno, lido=False, resposta=True).count(),
                    videos=videos,
                    submenu=curso,
                    is_tutorial=curso.is_tutorial,
                    menu='Prática Dinâmica' if curso.is_tutorial else 'cursos',
                    atividades=curso.atividades.filter().order_by('data_ini'),
                    tarefas=TarefaAtividade.objects.filter(aluno=aluno).exclude(correcao__exact="").exclude(
                        correcao__isnull=True)
                ))
        else:
            messages.error(request, 'Transação não disponível')
            raise PermissionDenied
    return render(request, 'painel-cursos.html', context)


@login_required
def tutorial(request):
    aluno = request.user.aluno
    pagina = request.GET.get('videos', 'cursos')
    context = {
        'menu': 'cursos',
        'aluno': aluno,
        'pagina': pagina,
    }

    if request.method == 'POST':
        if request.POST.get('todos_cursos') == 'on':
            context['filtro'] = True
    else:
        request.session['videos'] = request.GET.get('videos')
        if request.user.is_superuser:
            context['filtro'] = True

    if pagina == 'cursos':
        checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])
        context.update(dict(checkouts=checkouts))
    else:
        checkout_item = get_object_or_404(CheckoutItens, id=pagina)
        trans = checkout_item.checkout.transaction
        if trans:
            if trans.status not in ['pago', 'disponivel']:
                messages.error(request, 'Transação pendente')
                raise PermissionDenied
            else:
                curso_id = request.GET.get('curso_id')
                if curso_id:
                    curso = Curso.objects.get(id=curso_id)
                else:
                    curso = checkout_item.curso
                request.session['curso_id'] = curso.pk

                alunos = checkout_item.curso.get_alunos
                modulos = curso.modulo_set.all()
                videos = VideoModulo.objects.filter(modulo__in=modulos)

                if aluno not in alunos:
                    messages.error(request, 'Você não participa deste curso')
                    raise PermissionDenied
                context.update(dict(
                    todas_msg=PMensagem.objects.filter(curso=curso, aluno=aluno),
                    msg_naolidas=PMensagem.objects.filter(curso=curso, aluno=aluno, lido=False, resposta=True).count(),
                    videos=videos,
                    submenu=curso,
                    atividades=curso.atividades.all().order_by('data_ini'),
                    tarefas=TarefaAtividade.objects.filter(aluno=aluno).exclude(correcao__exact="").exclude(
                        correcao__isnull=True)
                ))
        else:
            messages.error(request, 'Transação não disponível')
            raise PermissionDenied
    return render(request, 'painel-cursos.html', context)



@login_required
def auto_correcao(request, pk):
    url = request.session.get("url")

    aluno = request.user.aluno
    atividade = Atividade.objects.get(pk=pk)
    try:
        tabelas = map(lambda x: x.valor, atividade.formulario.tabelas.all())
    except:
        tabelas = []
    sum_notas = soma_notas(aluno, atividade)
    context = {
        'menu': 'cursos',
        'submenu': atividade.nome,
        'atividade': atividade,
        'soma': sum(tabelas),
        'soma_notas': sum_notas,
        'url': url
    }
    if request.method == "POST":
        data = request.POST
        nota_ids = data.getlist("checkNota")
        tabela_id = data["tabela_id"]

        notas = NotaCorrecao.objects.filter(tabela_id=tabela_id, aluno=aluno)
        if notas:
            notas.delete()

        for nota_id in nota_ids:
            NotaCorrecao.objects.create(
                nota_id=nota_id, tabela_id=tabela_id, aluno=aluno
            )
        rev = reverse("aluno:auto_correcao", args=(pk,))
        return HttpResponseRedirect(rev)
    return render(request, 'aluno/auto_correcao/base.html', context)


def get_corrigir_json(request):
    from django.template import RequestContext
    req = RequestContext(request)
    try:
        tabela = Tabela.objects.get(id=request.GET.get('pk'))
        c = RequestContext(request, {"tabela": tabela})
        tarefa = render_to_string("aluno/auto_correcao/modal_corrigir.html", context=c)
    except Exception as e:
        tarefa = 'Erro: {0}'.format(e)
    return JsonResponse({'tarefa': tarefa})

@login_required
def simulados(request):
    aluno = request.user.aluno
    pagina = request.GET.get('videos', 'cursos')
    context = {
        'menu': 'cursos',
        'aluno': aluno,
        'pagina': pagina,
    }

    if request.method == 'POST':
        if request.POST.get('todos_cursos') == 'on':
            context['filtro'] = True
    else:
        request.session['videos'] = request.GET.get('videos')
    if pagina == 'cursos':
        checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])
        context.update(dict(checkouts=checkouts))
    else:
        checkout_item = get_object_or_404(CheckoutItens, id=pagina)
        trans = checkout_item.checkout.transaction
        if trans:
            if trans.status not in ['pago', 'disponivel']:
                messages.error(request, 'Transação pendente')
                raise PermissionDenied
            else:
                curso_id = request.GET.get('curso_id')
                if curso_id:
                    curso = Curso.objects.get(id=curso_id)
                else:
                    curso = checkout_item.curso
                request.session['curso_id'] = curso.pk

                alunos = checkout_item.curso.get_alunos
                modulos = curso.modulo_set.all()
                videos = VideoModulo.objects.filter(modulo__in=modulos)

                if aluno not in alunos:
                    messages.error(request, 'Você não participa deste curso')
                    raise PermissionDenied

                context.update(dict(
                    todas_msg=PMensagem.objects.filter(curso=curso, aluno=aluno),
                    msg_naolidas=PMensagem.objects.filter(curso=curso, aluno=aluno, lido=False, resposta=True).count(),
                    videos=videos,
                    submenu=curso,
                    atividades=curso.atividades.all().order_by('data_ini'),
                    tarefas=TarefaAtividade.objects.filter(aluno=aluno).exclude(correcao__exact="").exclude(
                        correcao__isnull=True)
                ))
        else:
            messages.error(request, 'Transação não disponível')
            raise PermissionDenied
    return render(request, 'painel-cursos.html', context)


@login_required
def sentencas_avulsas(request):
    aluno = request.user.aluno
    context = {
        'menu': 'Atividades Avulsas',
        'aluno': aluno,
        'todas_msg': PMensagem.objects.filter(aluno=aluno, sentenca=True),
    }
    filter = {
        'checkout__aluno': aluno,
        'curso__sentenca_avulsa__isnull': False,
        'checkout__transaction__status__in': ['pago', 'disponivel']
    }

    if request.method == 'GET':
        data = request.GET
        context['data'] = data

        # FILTROS
        # Expirado
        if not data.get('expirado') == 'on':
            filter['checkout__transaction__last_event_date__gte'] = timezone.now() - timedelta(days=365)
        # Categoria
        categoria = data.get('categoria')
        if categoria:
            filter['curso__categoria_id'] = categoria

    query_itens = CheckoutItens.objects.filter(**filter).distinct().order_by('-checkout__date')

    professores = []
    professores = [x.curso.sentenca_avulsa.professor for x in query_itens if
                   x.curso.sentenca_avulsa.professor not in professores and not professores.append(
                       x.curso.sentenca_avulsa.professor)]
    context['is_vdo'] = query_itens.filter(curso__sentenca_avulsa__video_id=True).exists()
    context["is_vdo"] = (
        query_itens.exclude(curso__sentenca_avulsa__video_id__isnull=True)
        .exclude(curso__sentenca_avulsa__video_id__exact="")
        .exists()
    )
    context['itens'] = query_itens
    context['professores'] = professores
    context['categorias'] = Categoria.objects.filter(tipo='S')

    if request.method == 'POST':
        st_id = request.POST.get('sentenca_id')
        sentenca = SentencaAvulsaAluno(
            sentenca_avulsa_id=st_id,
            aluno=aluno,

        )
        sentenca.save()
        messages.info(request, u'Sentença criada com sucesso !!!')
        return HttpResponseRedirect(reverse('curso:sentenca-responder', args=[sentenca.pk]))
    return render(request, 'painel-cursos-sentencas.html', context)


@login_required
def gabarito_autocorrecao(request):
    aluno = request.user.aluno
    context = {
        'menu': 'Gabaritos e Autocorreção',
        'aluno': aluno,
    }
    filtro = {}
    if request.method == 'POST':
        context['filtro'] = request.POST
    formularios = Formulario.objects.filter(**filtro)
    context['formularios'] = formularios
    return render(request, 'aluno/formulario_auto_correcao/gabaritos_autocorrecao.html', context)


@login_required
def creditos(request):
    aluno = request.user.aluno
    meus_creditos = Credito.objects.filter(aluno=aluno)
    configuracao_pacote = ConfiguracaoPacote.objects.filter(ativo=True).first()
    context = {
        'menu': 'Meus créditos',
        'aluno': aluno,
        'creditos': meus_creditos,
        'config': configuracao_pacote,
        'totais': Credito.totais(aluno_id=aluno.id)
    }

    if request.method == 'POST':
        cart = Cart(request.session)
        qtda = int(request.POST.get('qtda'))
        pacote_id = request.POST.get('pacote_id')
        valor = configuracao_pacote.valor_unitario * qtda
        if pacote_id and pacote_id != 'false':
            pacote = configuracao_pacote.pacotes.get(id=pacote_id)
            valor = pacote.valor
        else:
            pacote_desconto = configuracao_pacote.descontos.filter(ate__gte=qtda, de__lte=qtda).first()
            if pacote_desconto:
                cart.discount = (valor * Decimal(pacote_desconto.desconto)) / 100

        cart.add(
            configuracao_pacote.curso,
            price=valor,
            quantity=1,
            configuracao_pacote=configuracao_pacote.pk,
            quantidade=qtda,
            pacote=pacote_id
        )
        return HttpResponseRedirect(reverse('curso:carrinho'))
    return render(request, 'aluno/financeiro/credito.html', context)


@login_required
def creditos_resgates(request):
    pk = request.GET.get('pk')
    credito = get_object_or_404(Credito, pk=pk)

    context = {
        'credito': credito
    }

    return render(request, 'aluno/financeiro/credito-resgate.html', context)


@login_required
def creditos_comprar(request):
    context = {}
    return render(request, 'aluno/financeiro/modal_compra_pacote.html', context=context)


@login_required
def creditos_comprar_render(request):
    ctx = {'request': request}
    template = get_template('financeiro/comprar.html')
    context = Context(ctx)
    html = template.render(context)
    return JsonResponse({'html': html})


@login_required
def creditos_historico(request):
    aluno = request.user.aluno

    meus_creditos = Credito.objects.filter(aluno=aluno)

    filename = 'historico'

    for credito in meus_creditos:
        txt = u"ID DO PACOTE DATA DA AQUISIÇÃO DATA DE VENCIMENTO FORMA DE AQUISIÇÃO CRÉDITOS ADQUIRIDOS CRÉDITOS UTILIZADOS CRÉDITOS DISPONÍVEIS STATUS\n"
        txt += u"============ ================= ================== ================== =================== =================== ==================== ======\n"
        txt += u'{} {} {} {} {} {} {} {}\n'.format(
            credito,
            credito.created,
            credito.expire_date,
            credito.get_origem_display(),
            credito.quantidade,
            credito.utilizados,
            credito.disponivel,
            credito.status
        )

    response = HttpResponse(txt, content_type='text/plain; charset=utf8')
    response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(filename)
    return response


@login_required
def gabarito_autocorrecao_formulario(request, pk):
    aluno = request.user.aluno
    formulario = get_object_or_404(Formulario, pk=pk)
    respostas = RespostaAluno.objects.filter(aluno=aluno, tabela__formulario=formulario, nota__isnull=False)
    notas = map(lambda x: x.nota.valor, respostas)

    context = {
        'menu': 'Gabaritos e Autocorreção',
        'aluno': aluno,
        'formulario': formulario,
        'title': 'FORMULÁRIO PARA VOCÊ CORRIGIR SUA ATIVIDADE',
        'total': sum(notas)
    }
    return render(request, 'aluno/formulario_auto_correcao/pages/home.html', context)


@login_required
def gabarito_autocorrecao_formulario_corrigir(request, pk):
    aluno = request.user.aluno
    formulario = get_object_or_404(Formulario, pk=pk)
    context = {
        'menu': 'Gabaritos e Autocorreção',
        'aluno': aluno,
        'formulario': formulario,
        'title': 'FORMULÁRIO PARA VOCÊ CORRIGIR SUA ATIVIDADE'

    }
    return render(request,
                  'aluno/formulario_auto_correcao/pages/templates/aluno/formulario_auto_correcao/widgets/corrigir.html', context)


@login_required
def simuladoinfo(request, pk):
    aluno = request.user.aluno
    o_simuladoinfo = get_object_or_404(Simulado, pk=pk)
    cort = Cortesia.objects.filter(aluno=aluno, utilizado=True, curso__simulado=o_simuladoinfo).exists()
    cc = o_simuladoinfo.curso.checkoutitens_set.filter(
        curso=o_simuladoinfo.curso,
        checkout__aluno=aluno,
        checkout__transaction__status__in=['pago', 'disponivel']
    ).exists()
    if not cc | cort:
        raise PermissionDenied('Área restrita a professores')

    try:
        questionario_aluno = QuestionarioAluno.objects.get(
            simulado=o_simuladoinfo,
            aluno=aluno
        )
    except QuestionarioAluno.DoesNotExist:
        questionario_aluno = QuestionarioAluno.objects.none()

    # classificados = simuladoinfo.classificados()
    estatisticas = o_simuladoinfo.estatisticas()
    context = {
        'menu': 'Simulados',
        'submenu': o_simuladoinfo,
        'simulado': o_simuladoinfo,
        'curso': o_simuladoinfo.curso,
        'discuss': o_simuladoinfo.curso.get_discuss,
        'questionario_aluno': questionario_aluno,
        'estatisticas': estatisticas,
        'melhores': estatisticas[:3]
    }
    if questionario_aluno:
        context['questionario_estatisticas'] = questionario_aluno.estatisticas() \
            if questionario_aluno.data_conclusao else False

    return render(request, 'autor/painel-simulado.html', context)


@login_required
def simulados(request):
    aluno = request.user.aluno
    checkouts = CheckoutItens.objects.filter(checkout__aluno=aluno, curso__simulado__isnull=False,
                                             checkout__transaction__status__in=['pago', 'disponivel'])
    context = {
        'menu': 'Simulados',
        'aluno': aluno,
        'checkouts': checkouts
    }
    cortesias = []

    for cortesia in aluno.cortesia_set.filter(utilizado=True):
        cortesias.append(cortesia)
    context['cortesias'] = cortesias
    return render(request, 'painel-cursos-simulados.html', context)


@login_required
def sentencas_oab(request):
    aluno = request.user.aluno
    checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])
    context = {
        'menu': 'OAB 2ª Fase',
        'aluno': aluno,
        'checkouts': checkouts,
        'todas_msg': PMensagem.objects.filter(aluno=aluno, oab=True),
        'tem_sentencas': False
    }
    professores = []

    for checkout in checkouts:
        for x in checkout.get_sentencas_oab:
            context['tem_sentencas'] = True
            st = x.curso.sentenca_oab
            if st.professor not in professores:
                professores.append(st.professor)
    context['professores'] = professores

    if request.method == 'POST':
        st_id = request.POST.get('sentenca_id')
        sentenca = SentencaOABAvulsaAluno(
            sentenca_oab_id=st_id,
            aluno=aluno,

        )
        sentenca.save()
        messages.info(request, u'Peça criada com sucesso !!!')
        return HttpResponseRedirect(reverse('curso:sentenca-oab-responder', args=[sentenca.pk]))
    return render(request, 'painel-cursos-sentencas-oab.html', context)


@login_required
def video(request, vid):
    aluno = request.user.aluno
    vmodulo = get_object_or_404(VideoModulo, id=vid)
    check_itens = vmodulo.modulo.curso.checkoutitens_set.filter(checkout__aluno=aluno)
    checks = []
    for check in check_itens:
        trans = check.checkout.transaction
        if trans:
            if trans.status in ['pago', 'disponivel']:
                checks.append(check)
    if check:
        perm = False
        for x in map(lambda x: x.curso.modulo_set.all(), checks):
            if vmodulo.modulo in x:
                perm = True
        if not perm:
            raise PermissionDenied(u'Sem permissão para assistir o vídeo')
    else:
        raise PermissionDenied(u'Sem permissão para assistir o vídeo')
    context = {'video': vmodulo}
    if vmodulo.tipo == 'v':
        template = "painel-video-vdo.html"
        url = "https://dev.vdocipher.com/api/videos/%s/otp" % vmodulo.descricao
        context.update({"videoID": vmodulo.descricao})
        payloadStr = json.dumps({'ttl': 300})
        headers = {
            'Authorization': "Apisecret QPu1yL7eJ4A6JRzJV3KQbmDo6g5sviTdkzFRlRrhffoN3VbxC94tPYl7qYh7Kzxm",
            'Content-Type': "application/json",
            'Accept': "application/json"
        }

        response = requests.post(url, data=payloadStr, headers=headers)
        context.update(response.json())
    elif vmodulo.tipo == 'y':
        template = "painel-video-ytb.html"
    else:
        template = "painel-video.html"
    return render(request, template, context)


def perfil_aluno(request, aid):
    aluno = get_object_or_404(Aluno, id=aid, usuario__is_active=True)
    aluno_view = aluno_from_user_request(request)
    seguindo = False
    if aluno_view:
        seguindo = Seguir.objects.filter(de_aluno=aluno_view, para_aluno=aluno).first()
    context = {
        'menu': aluno,
        'aluno': aluno_view,
        'aluno_view': aluno,
        'seguindo': seguindo,
        'correcoes': Correcao.objects.filter(aluno=aluno).order_by('-data'),
    }
    return render(request, 'painel-perfil-aluno.html', context)


def busca_aluno(request):
    context = {
        'aluno': request.user.aluno
    }

    return render(request, 'painel-busca-aluno.html', context)


@login_required
def certificado(request):
    aluno = request.user.aluno
    context = {
        'aluno': aluno,
        'menu': 'certificados'
    }
    checkouts = aluno.checkout_set.filter(transaction__status__in=['pago', 'disponivel'])
    context.update(dict(checkouts=checkouts))
    return render(request, 'painel-certificado.html', context)


@login_required
def cupons(request):
    aluno = request.user.aluno
    context = {
        'aluno': aluno,
        'menu': 'cupons'
    }
    return render(request, 'painel-cupons.html', context)


@login_required
def certificado_solicitar(request, cid):
    aluno = request.user.aluno
    curso = get_object_or_404(Curso, pk=cid)
    ctx = {
        'aluno': aluno,
        'cpf': aluno.cpf,
        'curso': curso
    }
    # VALIDAR
    atividades_obrigatorias = curso.atividades.filter(resolucao_obrigatorio=True).count()
    tarefas = TarefaAtividade.objects.filter(aluno=aluno, atividade__curso=curso,
                                             atividade__resolucao_obrigatorio=True).count()
    cursos_do_aluno = curso.get_alunos

    err = False
    now = timezone.now().date()
    data_certificado = curso.certificado_data_ini
    if not data_certificado:
        msg = "O Administrador ainda não definiu uma data para a emissão do Certificado"
        err = True
        messages.error(request, msg)
    else:
        if curso.certificado_data_ini > now:
            msg = "O Certificado só poderá ser emitido a partir do dia {}".format(
                curso.certificado_data_ini.strftime('%d/%m/%Y')
            )
            err = True
            messages.error(request, msg)

    if aluno not in cursos_do_aluno:
        msg = "Você não faz parte desse curso"
        err = True
        messages.error(request, msg)

    if tarefas < atividades_obrigatorias / 2:
        msg = "Você respondeu {0} de um total de {1} Atividades. Responda 50% do total para " \
              "emitir o Certificado.".format(tarefas, atividades_obrigatorias)
        err = True
        messages.error(request, msg)
    if not aluno.cpf:
        msg = "Informa seu 'C.P.F' no menu 'Configurações' para poder emitir seu Certificado."
        err = True
        messages.error(request, msg)
    if not aluno.nome_completo:
        msg = "Informa seu 'Nome Completo' no menu 'Configurações' para poder emitir seu Certificado."
        err = True
        messages.error(request, msg)
    if err:
        return HttpResponseRedirect(reverse('aluno:certificado'))
    else:
        try:
            cert = Certificado.objects.get(aluno=aluno, curso=curso)
        except Certificado.DoesNotExist:
            cert = Certificado(aluno=aluno, curso=curso)
            try:
                cert.save()
            except IntegrityError:
                messages.error(request, "Erro ao gerar a chave! Tente Novamente.")
                return HttpResponseRedirect(reverse('aluno:certificado'))
    ctx['certificado'] = cert
    ctx['request'] = request
    template = get_template('certificado.html')
    context = Context(ctx)
    html = template.render(context)
    html = html.replace('{{aluno}}', aluno.nome_completo).replace('{{cpf}}', aluno.cpf)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@login_required
def timeline(request):
    aluno = request.user.aluno
    qnotificacoes = NotificacoesAluno.objects.filter(Q(para=aluno)).order_by('-data')

    context = {
        'menu': 'timeline',
        'aluno': aluno,
        'notificacoes': qnotificacoes
    }
    return render(request, 'painel-timeline.html', context)


@login_required
def notificacoes(request):
    aluno = request.user.aluno
    context = {
        'menu': 'notificações',
        'aluno': aluno,
    }

    filtro = request.GET.get('filtro', '')
    if filtro in ['C', 'M', 'L']:
        args = {'tipo': filtro}
    elif filtro == 'V':
        args = {'lido': False}
    elif filtro.startswith('id'):
        s = filtro.split(':')
        if len(s) > 1:
            filtro = 'id'
            context.update({'filtro_value': s[1]})
            qnotificacoes = NotificacoesAluno.objects.filter(id=s[1])
        else:
            filtro = ''
    else:
        args = {}

    if filtro != 'id':
        qnotificacoes = NotificacoesAluno.objects.filter(
            Q(para=aluno)
        ).exclude(status_resposta='I').filter(**args).order_by('-data')
    context.update({
        'filtro': filtro,
        'notificacoes': qnotificacoes
    })

    return render(request, 'painel-notificacoes.html', context)


@login_required
def painel(request):
    aluno = request.user.aluno
    context = {
        'menu': 'painel',
        'aluno': aluno,
        'respostas': Resposta.objects.filter(aluno=aluno, ativo=True, concluido=True).order_by('-data_termino')[:20],
        'avaliações': NotaResposta.objects.filter(aluno=aluno).order_by('-data')[:20]
    }

    grafico = {
        'resposta': {'QD': 0, 'PP': 0, 'ST': 0},
        'avaliacao': {'QD': 0, 'PP': 0, 'ST': 0},
        'correcao': {'QD': 0, 'PP': 0, 'ST': 0, 'total': 0},
        'corrigiram': {'QD': 0, 'PP': 0, 'ST': 0, 'total': 0},
        'total_QD': {'pontos': 0, 'porcento': 0},
        'total_PP': {'pontos': 0, 'porcento': 0},
        'total_ST': {'pontos': 0, 'porcento': 0}
    }
    # TOTAL RESPONDIDOS AGRUPADO POR TIPO
    total_geral = 0
    totres = aluno.get_total_respondidos()
    for r in totres:
        total_geral += r.get('total')
        grafico['resposta'][r.get('classificacao')] = r.get('total')
    # TOTAL CORREÇÃO AGRUPADO POR TIPO
    for c in aluno.get_total_corrigir():
        total_geral += c.get('total')
        grafico['correcao'][c.get('classificacao')] = c.get('total')
    # TOTAL CORRIGIRAM AGRUPADO POR TIPO
    for c in aluno.get_total_corrigirem():
        total_geral += c.get('total')
        grafico['corrigiram'][c.get('classificacao')] = c.get('total')

    if total_geral:
        # QD TOTAL/PORCENTO
        soma = grafico['resposta']['QD'] + grafico['correcao']['QD'] + grafico['corrigiram']['QD']
        grafico['total_QD']['pontos'] = soma
        grafico['total_QD']['porcento'] = (soma * 100) / total_geral
        # PP TOTAL/PORCENTO
        soma = grafico['resposta']['PP'] + grafico['correcao']['PP'] + grafico['corrigiram']['PP']
        grafico['total_PP']['pontos'] = soma
        grafico['total_PP']['porcento'] = (soma * 100) / total_geral
        # ST TOTAL/PORCENTO
        soma = grafico['resposta']['ST'] + grafico['correcao']['ST'] + grafico['corrigiram']['ST']
        grafico['total_ST']['pontos'] = soma
        grafico['total_ST']['porcento'] = (soma * 100) / total_geral
        a = {'total_PP': {'porcento': 0, 'pontos': 0},
             'total_ST': {'porcento': 0, 'pontos': 0},
             'total_QD': {'porcento': 75, 'pontos': 3},
             'resposta': {'PP': 0, 'total': 1, 'QD': 1, 'ST': 0},
             'correcao': {'PP': 0, 'total': 1, 'QD': 1, 'ST': 0},
             'corrigiram': {'PP': 0, 'total': 1, 'QD': 1, 'ST': 0}}
    context.update({'grafico': grafico})
    return render(request, 'painel-aluno.html', context)


@login_required
def mensagens(request):
    aluno = request.user.aluno
    de_alunos_msg = []
    todas_msg = Mensagem.objects.filter(Q(para_aluno=aluno) | Q(de_aluno=aluno))
    total = todas_msg.count()
    msg = Mensagem.objects.filter(para_aluno=aluno).values('de_aluno').annotate(total=Count('de_aluno')).order_by()

    for x in todas_msg.values('para_aluno', 'de_aluno').annotate(total=Count('de_aluno')).order_by():
        de_aluno = Aluno.objects.get(id=x.get('para_aluno'))
        if de_aluno == aluno:
            continue
        de_alunos_msg.append(
            dict(
                aluno=de_aluno,
                total=x.get('total'),
                nao_lidos=de_aluno.mensagem_dealuno.filter(para_aluno=aluno, lido=False).count()
            )
        )
    context = {
        'menu': u'Mensagens',
        'aluno': aluno,
        'de_alunos_msg': de_alunos_msg,
        'todas_msg': todas_msg,
        'total': todas_msg
    }
    return render(request, 'painel-mensagens.html', context)


@csrf_exempt
@login_required
def configuracoes(request):
    user = request.user
    aluno = user.aluno
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cancel':
            user.is_active = False
            user.save()
            messages.success(request, u'Cadastro cancelado.')
            return HttpResponseRedirect('/logout/')
        else:
            if request.FILES:
                foto = request.FILES.get('file_data')
                aluno.foto = foto
                aluno.save()
                return JsonResponse({'foto_url': aluno.foto_url})
            else:
                form = AlunoForm(request.POST, instance=aluno)
                if form.is_valid():
                    form.save()
                    messages.success(request, u'Dados atualizados.')
                else:
                    messages.error(request, u'Tente novamente.')
    else:
        form = AlunoForm(instance=aluno)

    context = {
        'menu': u'configurações',
        'aluno': aluno,
        'form': form,
    }
    return render(request, 'painel-configuracoes.html', context)


@login_required
def get_message(request):
    aluno = request.user.aluno
    de_id = request.GET.get('id')
    msg = []
    todas_msg = Mensagem.objects.filter(
        Q(Q(de_aluno_id=de_id) & Q(para_aluno=aluno)) | Q(Q(para_aluno_id=de_id) & Q(de_aluno=aluno)))
    for mensagem in todas_msg:
        msg.append(dict(
            aluno_id=mensagem.de_aluno.id,
            aluno=mensagem.de_aluno.nome,
            texto=mensagem.html,
            aluno_url=mensagem.de_aluno.get_absolute_url(),
            img_url=mensagem.de_aluno.foto_url,
            data=mensagem.str_data,
            lido=mensagem.lido,
            mensagem_id=mensagem.id

        ))
    return JsonResponse(msg, safe=False)


@csrf_exempt
def busca_aluno_json(request):
    ret = []
    for aluno in Aluno.objects.all():
        ret.append({
            'name': aluno.nome,
            'foto': aluno.foto_url
        })
    return JsonResponse(ret, safe=False)


@login_required
def meus_desafios(request):
    context = {
        'menu_ativo': 'meus-desafios',
        'aluno': request.user.aluno
    }
    return render(request, 'perfil-desafios.html', context)


def cadastro(request):
    form = CadastroAlunoForm()
    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # remover chaves da var 'data' que não pertencem ao model 'Aluno'
            password = data.pop('password')
            data.pop('password2')
            # Criar Usuário
            email = data.get('email')
            newsletter = data.get('newsletter')
            first_name = split_name(data.get('nome'))
            last_name = split_name(data.get('nome'), True)
            user = User.objects.create_user(
                email, email, password, first_name=first_name, last_name=last_name
            )
            data.update({'usuario_id': user.id})
            data.update({'newsletter': newsletter})

            # CRIAR ALUNO
            aluno = Aluno(**data)
            aluno.save()
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('aluno:perfil'))

    context = {'form': form}
    return render(request, 'cadastro.html', context)


@login_required
def discussao(request, pk):
    discuss = get_object_or_404(Discussao, id=pk)
    check = CheckoutItens.objects.filter(
        curso=discuss.curso,
        checkout__aluno=request.user.aluno
    ).first()
    context = {
        'discuss': discuss,
        'menu': u'Discussão',
        'submenu': discuss,
        'aluno': request.user.aluno,
        'check': check,
        'backto': request.GET.get('backto')
    }
    return render(request, 'painel-cursos-discussao.html', context)
