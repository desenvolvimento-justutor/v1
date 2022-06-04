# -*- coding: utf-8 -*-
# Autor: christian
import os
from datetime import timedelta, datetime, time

from django.core.management.base import BaseCommand
from django_comments.models import Comment
from django_extensions.management.color import color_style

from apps.curso.models import Curso
from apps.curso.models import Discussao, DocCurso, Atividade, CheckoutItens
from apps.website.utils import enviar_email
from justutorial.settings import BASE_DIR
from libs.util.mail import send_mail

class Command(BaseCommand):

    help = 'Notifica os alunos por email sobre novas atividades no Curso'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data', '-d', action='store', dest='data',
            help='Data formato: d/m/Y'
        )
        parser.add_argument(
            '--email', '-m', action='store', dest='email',
            help='S para enviar'
        )
        parser.add_argument(
            '--email-teste', '-t', action='store', dest='email_teste',
            help='S para enviar'
        )

    def handle(self, *args, **options):
        self.style = color_style()
        email = options.get('email')
        email_teste = options.get('email_teste')
        # CURSOS
        cursos = Curso.objects.filter(sentenca_avulsa__isnull=True, sentenca_oab__isnull=True)
        # DATAS
        data = options.get('data')
        if data:
            today = datetime.strptime(data, '%d/%m/%Y')
        else:
            today = datetime.now()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        # INTERVALO DE DATAS
        dates = (
            datetime.combine(yesterday, time.min),
            datetime.combine(yesterday, time.max)
        )
        self.stdout.write(self.style.URL_NAME(u'HOJE..: %s' % self.style.BOLD(today)))
        self.stdout.write(self.style.URL_NAME(u'ONTEM.: %s' % self.style.BOLD(yesterday)))
        self.stdout.write(self.style.URL_NAME(u'AMANHÃ: %s' % self.style.BOLD(tomorrow)))
        # LOOP NO CURSO
        for curso in cursos:
            discuss_ids = map(lambda x: x.pk, curso.discussao_set.all())
            comentarios = Comment.objects.for_model(Discussao).filter(submit_date__range=dates, object_pk__in=discuss_ids)
            materiais = DocCurso.objects.filter(data_ativo=yesterday, curso=curso)
            atividades = Atividade.objects.filter(data=yesterday, curso=curso)
            atividades_vencer = Atividade.objects.filter(data_fim=tomorrow, curso=curso)
            checkout_item = CheckoutItens.objects.filter(curso=curso).first()
            # EMAILS
            if email_teste:
                emails_alunos = [email_teste]
            else:
                emails_alunos = map(lambda x: x.email, curso.get_alunos)

            if comentarios or materiais or atividades or atividades_vencer:
                s = u"{0}: {1}\n".format(today, curso.nome)
                with open(os.path.join(BASE_DIR, "notificar.log"), "a") as myfile:
                    myfile.write(s.encode('utf-8'))

                self.stdout.write(self.style.INFO('=' * 80))
                self.stdout.write(self.style.WARN(u'Curso.: %s' % self.style.BOLD(u'%s' % curso)))
                self.stdout.write(self.style.WARN(u'Emails: %s' % self.style.BOLD('%03d' % len(emails_alunos))))
                self.stdout.write(self.style.INFO(';'.join(emails_alunos)))
                self.stdout.write(self.style.INFO('-' * 80))

                if comentarios or materiais or atividades:
                    ctx_email = {
                        'curso': curso, 'yesterday': yesterday, 'checkout': checkout_item
                    }
                    if comentarios:
                        self.stdout.write(
                            self.style.URL_NAME(u'Comentários: %s' % self.style.BOLD('%03d' % len(comentarios)))
                        )
                        discuss = {}
                        for comentario in comentarios:
                            d = Discussao.objects.get(id=comentario.object_pk)
                            if d not in discuss:
                                discuss[d] = [comentario]
                            else:
                                discuss[d].append(comentario)
                        ctx_email['discuss'] = discuss

                    if materiais:
                        self.stdout.write(
                            self.style.URL_NAME(u'Materiais..: %s' % self.style.BOLD('%03d' % len(materiais)))
                        )
                        ctx_email['materiais'] = materiais
                    if atividades:
                        self.stdout.write(
                            self.style.URL_NAME(u'Atividades.: %s' % self.style.BOLD('%03d' % len(atividades)))
                        )
                        ctx_email['atividades'] = atividades
                    # ENVIAR EMAIL PARA OS ALUNOS
                    if email in ['S', 's']:

                        from django.core import mail
                        connection = mail.get_connection()
                        connection.open()

                        for email_aluno in emails_alunos:
                            try:
                                curso_title = 'simulado' if curso.categoria.tipo == 'D' else 'curso'
                                enviar_email(
                                    'curso/email/notificar-aluno.html',
                                    u'[{0:02d}/{1:02d}] Relatório de atividades do seu {2} "{3}"'.format(
                                        today.day, today.month, curso_title, curso.nome
                                    ), [email_aluno], ctx_email, ead=True
                                )
                            except Exception as e:
                                self.stdout.write(self.style.URL_NAME(u'Erro: {}'.format(e)))

                if atividades_vencer:
                    self.stdout.write(
                        self.style.URL_NAME(u'Atv. Vencer: %s' % self.style.BOLD('%03d' % len(atividades_vencer)))
                    )
                    # ENVIAR EMAIL PARA OS ALUNOS
                    if email in ['S', 's']:
                        ctx_email = {
                            'curso': curso, 'tomorrow': tomorrow, 'checkout': checkout_item,
                            'atividades': atividades_vencer
                        }
                        for email_aluno in emails_alunos:
                            enviar_email(
                                'curso/email/notificar-aluno-atividades.html',
                                u'[{0:02d}/{1:02d}] Aviso de prazo vencendo no seu curso "{2}"'.format(
                                    today.day, today.month, curso
                                ), [email_aluno], ctx_email, ead=True
                            )
                            self.stdout.write(self.style.INFO(u"Atividade enviada para '{}'".format(email_aluno)))
