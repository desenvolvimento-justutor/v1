# Author: Christian Douglas <christian.douglas.alcantara@gmail.com>
from threading import Thread

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from apps.curso.models import Curso
from django.utils import timezone
from apps.cupom.models import Cupom
from decimal import Decimal
from django.contrib import messages
from apps.aluno.models import Aluno
from libs.util import shortuuid
from django.db import transaction


def criar_cupom(tipo, valor, data, produto, aluno, prefixo=False):
    if prefixo:
        codigo = '{}{}'.format(prefixo, shortuuid.uuid()[:7].upper())
    else:
        codigo = shortuuid.uuid()[:10].upper(),

    data = {
        'codigo': codigo,
        'tipo': tipo,
        'data_limite': data,
        'qte_max_uso': 1,
        'cliente': aluno
    }
    if tipo == 'Nominal (Valor)':
        data.update({'valor_desconto': valor})
    else:
        data.update({'percentual_desconto': valor})

    cupom = Cupom.objects.create(**data)
    cupom.produtos.add(produto)
    cupom.save()
    return cupom


class MyThread(Thread):

    def __init__(self, tipo, valor, data, produto, alunos, prefixo=False):
        # super(MyThread, self).__init__(produto, data)
        self.tipo = tipo
        self.valor_desconto = valor
        self.validade = data
        self.curso_novo = produto
        self.alunos = alunos
        self.prefixo = prefixo
        Thread.__init__(self)

    def run(self):
        with transaction.atomic():
            for aluno in self.alunos:
                criar_cupom(self.tipo, self.valor_desconto, self.validade, self.curso_novo, aluno, self.prefixo)
        return


def get_alunos_curso_json(cursos_id):
    cursos = Curso.objects.filter(id__in=cursos_id)
    alunos = []
    for ocurso in cursos:
        for aluno in ocurso.get_alunos:
            if aluno not in alunos:
                alunos.append(aluno)
    return alunos

@login_required
def gerarcupons(request):
    """
    If you're using multiple admin sites with independent views you'll need to set
    current_app manually and use correct admin.site
    # request.current_app = 'admin'
    """
    context = admin.site.each_context(request)
    now = timezone.now()

    context.update({
        'title': 'Gerar cupons',
        'cursos_inativos': Curso.objects.filter(data_fim__lt=now),
        'cursos_novos': Curso.objects.filter(data_fim__gt=now)
    })
    if request.method == 'POST':
        data = request.POST
        try:
            cursos_id = data.getlist('curso_anterior')
            # id_alunos = data.getlist('alunos')
            alunos = get_alunos_curso_json(cursos_id)
            tipo = data.get('tipo')
            prefixo = data.get('prefixo')
            validade = datetime.strptime('{} 23:59'.format(data.get('validade')), '%Y-%m-%d %H:%M')
            valor_desconto = Decimal(data.get('valor_desconto'))
            curso_novo = Curso.objects.get(id=data['curso_novo'])
            th = MyThread(tipo, valor_desconto, validade, curso_novo, alunos, prefixo)
            th.start()
            messages.info(request, '[{}] Cupons gerados'.format(len(alunos)))
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'admin/mass_coupon.html', context)
