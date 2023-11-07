# -*- coding: utf-8 -*-
import StringIO
import csv
import io
from decimal import Decimal

from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from apps.formulario_correcao.models import TabelaCorrecaoAluno, Tabela, Formulario, Nota
from .models import Nota


@login_required
def relatorio(request):
    kwargs = {"corrigido": True}
    if request.method == "POST":
        professor_id = request.POST.get("professor_id")
        pago_id = request.POST.get("pago_id")
        if professor_id:
            kwargs["professor_id"] = professor_id
        if pago_id:
            kwargs["pago"] = True if pago_id == "1" else False
        print(">>>>", kwargs)
        print(">>>>", request.POST)
        tabelas = TabelaCorrecaoAluno.objects.filter(
            **kwargs
        ).values('professor__nome', 'formulario__titulo').annotate(
            total=Count('formulario')
        ).order_by('professor', 'total')

        txt = "{:40s} {:110s} {}\n".format("Professor", "Formulario", "Total")
        txt += "{} {} {}\n".format("=" * 40, "=" * 110, "=====")
        count = 0
        for tabela in tabelas:
            nome = tabela["professor__nome"] or ""
            if nome:
                nome = nome.encode("utf-8")
            txt += "{:40s} {} {:05d}\n".format(nome, tabela["formulario__titulo"].ljust(110, ".").encode("utf-8"),
                                               tabela["total"])
            count += tabela["total"]
        txt += "{} {} {}\n".format("=" * 40, "=" * 110, "=====")
        txt += "{:40s} {:>110} {:05d}".format("", "Total:", count)
        response = HttpResponse(txt, content_type='text/plain; charset=utf8')
        response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format("relatorio")
        return response
    else:
        return HttpResponseRedirect("/admin/formulario_correcao/tabelacorrecaoaluno/")


def csv_to_list_in_memory(filename):
    file = filename.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))
    # Gerando uma list comprehension
    data = [line for line in reader]
    return data


@login_required
def gerarnotas(request):
    context = {
        "title": "Gerar Notas"
    }
    if request.method == 'POST' and request.FILES.get("csv_file"):
        csv_file = request.FILES.get("csv_file")
        csv_fo = StringIO.StringIO(csv_file.read())
        inc = 1
        for line in csv.DictReader(csv_fo, delimiter=';'):
            try:
                vals = {
                    "unica": True if line["unica"] == "1" else False,
                    "titulo": line["titulo"].decode("utf-8")[:199],
                    "texto": line["texto"].decode("utf-8"),
                    "valor": Decimal(line["valor"].replace(",", "."))
                }
                with transaction.atomic():
                    Nota.objects.create(**vals)
            except Exception as e:
                messages.error(request, str(e) + "/ LINHA=" + str(inc))
            inc += 1
        return HttpResponseRedirect("/admin/formulario_correcao/nota/")
    return render(request, 'admin/gerar_notas.html', context=context)


def remove_chars(value):
    new = value.replace("\t", "").replace("\n", "").replace("\r", "")
    return new


@login_required
def import_formulario_correcao(request):
    context = {
        "title": u"Importar Formulário de Correção"
    }
    if request.method == 'POST' and request.FILES.get("html_file"):
        formulario_id = request.POST.get("formulario_id")
        try:
            formulario_id = Formulario.objects.get(id=formulario_id)
        except Formulario.DoesNotExist:
            messages.error(request, u"O Formulário com ID: %s, não existe" % formulario_id)
        else:
            try:
                html_file = request.FILES.get("html_file")
                file_read = StringIO.StringIO(html_file.read())

                contents = file_read.read()

                soup = BeautifulSoup(contents, 'lxml')

                tables = soup.find_all("table")
                order = 0
                for table in tables:
                    tds = table.find_all("td")
                    titulo = remove_chars(tds[0].text)

                    comentario = ""
                    for p in tds[1].find_all("p"):
                        comentario += remove_chars(str(p))

                    valor = 0
                    notas = []
                    if len(tds) == 3:
                        try:
                            nota_code, valor_text = remove_chars(tds[2].text).split(";")
                        except ValueError:
                            messages.error(request, u"Verifique a linha: %s" % tds[2].text)
                            continue
                        notas = Nota.objects.filter(titulo__startswith=nota_code)
                        valor = Decimal(valor_text)
                        if not notas:
                            messages.warning(request, u"Nota com o código [%s] não encontrada." % nota_code)
                    else:
                        messages.warning(request, u"Tabela [%s] não possui a linha com a Nota." % titulo)

                    try:
                        with transaction.atomic():
                            tabela = Tabela.objects.create(
                                formulario=formulario_id,
                                valor=valor,
                                item=titulo,
                                comentarios=comentario,
                                order=order
                            )
                            if notas:
                                tabela.nota.add(*notas)
                            order += 1
                    except Exception as e:
                        messages.error(request, "1: " + str(e))
            except Exception as e:
                messages.error(request, "2: " + str(e))
        return HttpResponseRedirect("/admin/formulario_correcao/tabela/")

    return render(request, 'admin/importar_formulario_correcao.html', context=context)
