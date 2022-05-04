# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from apps.pagseguro.models import Checkout
from django.db.models import Q
from django_extensions.management.color import color_style


class Command(BaseCommand):
    help = """Verifica transações do pagseguro"""

    def handle(self, *args, **options):
        self.style = color_style()
        q = [
            Q(transaction_code__isnull=False),
            Q(transaction_status__in=[1, 2, 4, 5, 6]) |
            Q(transaction_status__isnull=True)
        ]
        self.stdout.write(self.style.WARN(u'Curso.: %s' % self.style.BOLD(u'%s' % u'VERIFICANDO TRANSAÇÃO')))
        for checkout in Checkout.objects.filter(*q):
            # try:
            tstatus_atual = checkout.get_transaction_status_display()
            status_code = checkout.get_transaction_status()
            tstatus_novo = checkout.get_transaction_status_display()
            code = checkout.transaction_code
            log = u"[{status:}] {code:}: {atual:} -> {novo:}".format(
                status=status_code, code=code, atual=tstatus_atual, novo=tstatus_novo
            )
            self.stdout.write(self.style.INFO(u'INFO.: %s' % self.style.BOLD(u'%s' % log)))
        # except Exception as e:
            #     self.stdout.write(self.style.WARN(u'ERRO.: %s' % self.style.BOLD(u'%s' % e)))
        self.stdout.write(self.style.WARN(u'Curso.: %s' % self.style.BOLD(u'%s' % u'VERIFICAÇÃO CONCLUÍDA')))