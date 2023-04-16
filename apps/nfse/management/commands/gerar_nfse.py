# -*- coding: utf-8 -*-
# Autor: christian

from django.core.management.base import BaseCommand
from django_extensions.management.color import color_style
from apps.pagseguro.models import Checkout


class Command(BaseCommand):
    help = 'Gerar e enviar NFSe'

    def handle(self, *args, **options):
        self.style = color_style()

        del_chechouts = Checkout.objects.filter(
            aluno__isnull=True,
            transaction_type__isnull=True,
            transaction_status__isnull=True)
        self.stdout.write(self.style.URL_NAME(u'Deletadas..: %s' % self.style.BOLD(del_chechouts.count())))
        chechouts = Checkout.objects.filter(
            date__gte="2023-04-13 00:00:00",
            transaction_status=3,
            nfse__isnull=True
        )
        for checkout in chechouts:
            self.stdout.write(
                self.style.URL_NAME(u'Enviando...: %s' % self.style.BOLD("%s - %s" % (checkout.id, checkout.date))))
            checkout.incluir_os()
        self.stdout.write(self.style.URL_NAME(u'Total......: %s' % self.style.BOLD(chechouts.count())))
