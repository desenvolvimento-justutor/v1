# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import Signal

from dateutil.parser import parse
import json
from apps.website.utils import enviar_email

from .settings import TRANSACTION_STATUS
from apps.aluno.models import Aluno
import logging

logger = logging.getLogger("apps")

checkout_realizado = Signal(providing_args=['data'])
checkout_realizado_com_sucesso = Signal(providing_args=['data'])
checkout_realizado_com_erro = Signal(providing_args=['data'])

notificacao_recebida = Signal(providing_args=['transaction'])
notificacao_status_aguardando = Signal(providing_args=['transaction'])
notificacao_status_em_analise = Signal(providing_args=['transaction'])
notificacao_status_pago = Signal(providing_args=['transaction'])
notificacao_status_disponivel = Signal(providing_args=['transaction'])
notificacao_status_em_disputa = Signal(providing_args=['transaction'])
notificacao_status_devolvido = Signal(providing_args=['transaction'])
notificacao_status_cancelado = Signal(providing_args=['transaction'])


NOTIFICATION_STATUS = {
    '1': notificacao_status_aguardando,
    '2': notificacao_status_em_analise,
    '3': notificacao_status_pago,
    '4': notificacao_status_disponivel,
    '5': notificacao_status_em_disputa,
    '6': notificacao_status_devolvido,
    '7': notificacao_status_cancelado
}

def save_checkout(sender, data, **kwargs):
    from .models import Checkout
    transaction = data.get('transaction', '')
    reference = transaction.get('reference', '')
    checkout = Checkout(
        date=data.get('date'),
        success=data.get('success'),
        message=data.get('response'),
    )
    if ':' in reference:
        aluno_pk, cpf = reference.split(':')
        try:
            checkout.aluno = Aluno.objects.get(pk=aluno_pk)
        except:
            pass
        checkout.cpf = cpf

    if checkout.success:
        checkout.code = data.get('code')
    else:
        checkout.message = data.get('message')

    checkout.save()
    checkout.get_transaction_status()
    # update_transaction(sender, data, **kwargs)


def update_items(items, checkout):
    from apps.curso.models import CheckoutItens, Curso
    new_itens = items
    checkout_items = checkout.checkoutitens_set.all()
    if not checkout_items:
        if not isinstance(items, list):
            new_itens = [items]
        for item in new_itens:
            try:
                curso = Curso.objects.get(pk=int(item['id']))
                if curso.categoria.tipo == 'B':
                    CheckoutItens.objects.create(
                        checkout=checkout,
                        curso=curso,
                        qtda=item['quantity'],
                        valor=item['amount']
                    )
                    cursos = curso.cursos.all()
                    for cur in cursos:
                        CheckoutItens.objects.create(
                            checkout=checkout,
                            curso=cur,
                            qtda=1,
                            valor=0
                        )
                else:
                    CheckoutItens.objects.create(
                        checkout=checkout,
                        curso=curso,
                        qtda=item['quantity'],
                        valor=item['amount']
                    )
            except Exception as e:
                raise e
    return checkout_items


def update_checkout(data, transaction):
    from .models import Checkout
    items = data.get('items')['item']
    code = data.get('code')
    reference = data.get('reference', '')

    try:
        checkout = Checkout.objects.get(transaction_code=code)
    except Checkout.DoesNotExist:
        checkout = Checkout(
            code=code,
            transaction_code=code,
            date=parse(data.get('date')),
            success=True,
            message=json.dumps(data, indent=2),
        )
    if ':' in reference:
        aluno_pk, cpf = reference.split(':')
        try:
            checkout.aluno = Aluno.objects.get(pk=aluno_pk)
        except:
            pass
        checkout.cpf = cpf
    checkout.save()
    if not transaction.checkout:
        transaction.checkout = checkout
        transaction.save()
    checkout.get_transaction_status()
    update_items(items, checkout)
    try:
        logger.debug('[INCLUIR_OS] status code: {}'.format(checkout))
        checkout.incluir_os()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(tb)
        enviar_email(
            'curso/email/nfs.html',
            'Erro ao gerar NFs!',
            ['christian.dev.py@gmail.com'],
            context={'checkout': checkout, "mensagem": tb},
            ead=False
        )
    return checkout


def update_transaction(sender, transaction, **kwargs):
    from .models import Transaction, TransactionHistory, Checkout

    trans = transaction

    try:
        transaction = Transaction.objects.get(code=trans.get('code'))
    except Transaction.DoesNotExist:
        transaction = Transaction.objects.create(
            code=trans.get('code'),
            status=TRANSACTION_STATUS[trans.get('status')],
            date=parse(trans.get('date')),
            last_event_date=parse(trans.get('lastEventDate')),
            content=json.dumps(trans, indent=2),
            reference=trans.get('reference', '')
        )
    transaction.status = TRANSACTION_STATUS[trans.get('status')]
    transaction.last_event_date = parse(trans.get('lastEventDate'))
    transaction.content = json.dumps(trans, indent=2)
    transaction.save()
    TransactionHistory.objects.create(
        transaction=transaction,
        status=TRANSACTION_STATUS[trans.get('status')],
        date=parse(trans.get('lastEventDate'))
    )
    update_checkout(trans, transaction)
    # update_items(trans.get('items'), data)
