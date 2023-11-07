# -*- coding: utf-8 -*-
# Autor: christian

from django.core.management.base import BaseCommand
from django_extensions.management.color import color_style
from apps.pagseguro.models import Checkout


class Command(BaseCommand):
    help = 'Gerar e enviar NFSe'

    def add_arguments(self, parser):
        parser.add_argument(
            '--gerar', '-g', action='store', dest='gerar'
        )
        parser.add_argument(
            '--delete', '-d', action='store', dest='delete'
        )

    def handle(self, *args, **options):
        self.style = color_style()
        gerar = options.get('gerar')
        delete = options.get('delete')

        del_chechouts = Checkout.objects.filter(
            aluno__isnull=True,
            transaction_type__isnull=True,
            transaction_status__isnull=True)
        self.stdout.write(self.style.URL_NAME(u'Deletadas..: %s' % self.style.BOLD(del_chechouts.count())))

        if delete:
            del_chechouts.delete()
        chechouts = Checkout.objects.filter(
            date__gte="2023-07-01 00:00:00",
            transaction_status=3,
            nfse__isnull=True
        )
        count = error = 0
        for checkout in chechouts:
            self.stdout.write(
                self.style.URL_NAME(u'Enviando...: %s' % self.style.BOLD("%s - %s" % (checkout.id, checkout.date))))
            if gerar == "y":
                try:
                    nfse = checkout.incluir_os()
                    if nfse:
                        count += 1
                    else:
                        error += 1
                except Exception as e:
                    error += 1
                    self.stdout.write(self.style.WARN(u'%s' % str(e)))
        self.stdout.write(self.style.INFO(u'Total......: %s' % self.style.BOLD(count)))
        self.stdout.write(self.style.WARN(u'Erros......: %s' % self.style.BOLD(error)))
