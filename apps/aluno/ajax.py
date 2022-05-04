# coding=utf-8
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
import re
from cepbr import CEP
from .processor import proc_aluno
from apps.enunciado.models import NotificacoesAluno
from .models import Aluno, Mensagem, Seguir
from justutorial.settings import push
from apps.website.utils import enviar_email
from django.contrib import messages

@dajaxice_register(method='GET')
def get_cep(request, cep):
    x = Dajax()
    c = CEP()
    cep = re.sub("[-/.]", "", cep)
    data = {}
    try:
        data = c.get_cep(cep)
    except Exception as e:
        x.script("BootstrapDialog.alert('{0}');".format(str(e)))
        x.script(u"$('#id_cep').val('')")

    x.script(u"$('#id_logradouro').val('{0}')".format(data.get('logradouro', '')))
    x.script(u"$('#id_bairro').val('{0}')".format(data.get('bairro', '')))
    x.script(u"$('#id_cidade').val('{0}')".format(data.get('localidade', '')))
    x.script(u"$('#id_uf').val('{0}')".format(data.get('uf', '')))
    x.script("unBlockFunction()")
    return x.json()


@dajaxice_register(method='GET')
def set_lido(request, nid):
    x = Dajax()
    # Marcar notificação como lido
    n = NotificacoesAluno.objects.get(id=nid)
    n.lido = True
    n.save()
    # Atualizar tela
    i = proc_aluno(request).get('proc_aluno').get('notificacoes').count()
    if i >= 1:
        html = '<span class="text-success"><i data-placement="left" data-toggle="tooltip" title="Marcada como já ' \
               'visualizada" class="fa fa-eye fa-lg pull-right"></i></span>'
        x.script("""$("#icone-lido-{0}").html('{1}');""".format(nid, html))
        x.script("""$('#id-notificacao-menu-item-{0}').remove()""".format(nid))
        x.script("""$('#id-notificacao-menu-esq').html({0})""".format(i))
        x.script("""$('#id-notificacao-menu-count').html({0})""".format(i))
        x.script("""$('#id-notificacao-menu-info').html({0})""".format(i))
    else:
        x.script("""$('#id-notificacao-menu').remove()""")
        x.script("""$('#id-notificacao-menu-esq').remove()""")
    x.script('_toastr("Notificação marcada como Visualizada.","top-right","success",false);')
    return x.json()


@dajaxice_register(method='GET')
def msg_set_lido(request, mid):
    x = Dajax()
    aluno = request.user.aluno
    # Marcar notificação como lido
    n = Mensagem.objects.get(id=mid)
    n.lido = True
    n.save()
    # Atualizar tela
    i = aluno.msg_para_naolidas.count()
    html = '<span class="text-success"><i data-placement="left" data-toggle="tooltip" title="Marcada como' \
           'visualizada" class="fa fa-check fa-lg pull-right"></i></span>'
    x.script("""$("#icone-lido-{0}").html('{1}');""".format(mid, html))
    x.script("""$('#id-msg-menu-esq').html({0})""".format(i))
    x.script("""$('#id-msg-count-{0}').html({1})""".format(n.de_aluno.id,
        n.de_aluno.mensagem_dealuno.filter(para_aluno=aluno, lido=False).count())
    )
    if not i:
        x.script("""$('#id-msg-menu-esq').remove()""")
        x.script("""$('#id-msg-count-{0}').remove()""".format(n.de_aluno_id))
    x.script('_toastr("Mensagem marcada como Visualizada.","top-right","success",false);')
    x.script('stopLoad()')
    return x.json()


@dajaxice_register(method='GET')
def ativar_notificacao(request, notificacao, valor):
    x = Dajax()
    aluno = request.user.aluno

    if valor:
        css_class = 'info'
        msg = u'Você ativou receber: <strong>{0}</strong>'
    else:
        css_class = 'warning'
        msg = u'Você desativou receber: <strong>{0}</strong>'

    if notificacao == 'checkbox-notificar-correcao':
        msg = msg.format(u'Correções de suas respostas por e-mail.')
        aluno.notificar_correcao = valor
    elif notificacao == 'checkbox-notificar-comentario':
        msg = msg.format(u'Comentários de suas correções por e-mail.')
        aluno.notificar_comentario = valor
    elif notificacao == 'checkbox-notificar-avaliacao':
        msg = msg.format(u'Curtidas de suas correções por e-mail.')
        aluno.notificar_avaliacao = valor
    elif notificacao == 'checkbox-notificar-seguir':
        msg = msg.format(u'Seguidores por e-mail.')
        aluno.notificar_seguir = valor
    elif notificacao == 'checkbox-notificar-responder-seguir':
        msg = msg.format(u'Seguidores por e-mail.')
        aluno.notificar_responder_seguir = valor
    else:
        x.script('_toastr("Opção Inválida","top-right","error",false);')
        return x.script()
    aluno.save()
    x.script(u'_toastr("{0}","top-right","{1}",false);'.format(msg, css_class))
    return x.json()

@dajaxice_register(method='GET')
def seguir(request, aid, acao):
    x = Dajax()
    aluno = request.user.aluno
    para_aluno = Aluno.objects.get(id=aid)
    if acao == 'True':
        s = Seguir(de_aluno=aluno, para_aluno=para_aluno)
        s.save()
        x.script('$("#btn-seguir").prop("class", "btn btn-danger fa fa-user-times pull-right")')
        x.script('$("#btn-seguir").data("seguir", "False").prop("data-tooltip", "tooltip")')
        x.script('$("#btn-seguir").prop("title", "Deixar de Seguir")')
        x.script(u'_toastr("Seguindo: {0}","top-right","success",false);'.format(para_aluno))
        push.trigger('painel_channel', 'notificar_aluno', {
            'message': '{0} Começou a te seguir'.format(aluno),
            'aluno_id': para_aluno.id
        })
        if para_aluno.notificar_seguir:
            ctx = {'aluno': aluno}
            enviar_email(
                'email/email-seguir.html', u'Você tem um novo seguidor no JusTutor', [para_aluno.email], ctx
            )
    else:
        try:
            s = Seguir.objects.get(de_aluno=aluno, para_aluno=para_aluno)
            s.delete()
            x.script('$("#btn-seguir").prop("class", "btn btn-success fa fa-user-plus pull-right")')
            x.script('$("#btn-seguir").data("seguir", "True").prop("data-tooltip", "tooltip")')
            x.script('$("#btn-seguir").prop("title", "Seguir")')
            x.script(u'_toastr("Deixou de seguir: {0}","top-right","error",false);'.format(para_aluno))
            push.trigger('painel_channel', 'notificar_aluno', {
                'message': '{0} Deixou de te seguir'.format(aluno),
                'aluno_id': para_aluno.id
            })
        except Exception as e:
            x.script(u'_toastr("ERRO: {0}","top-right","error",false);'.format(e))

    x.script('$("#btn-seguir").button("reset")')
    return x.json()


@dajaxice_register(method='GET')
def enviar_mensagem(request, aid, mensagem):
    print '************', aid, mensagem
    x = Dajax()
    try:
        de = request.user.aluno
        para = Aluno.objects.get(id=aid)
        msg = Mensagem(de_aluno=de, para_aluno=para, mensagem=mensagem)
        msg.save()
        x.script('_toastr("Sua mensagem foi enviada.","top-right","success",false);')
    except Exception as e:
        print '************', e
        raise e
        # import os
        # from justutorial.settings import BASE_DIR
        # fl = os.path.join(BASE_DIR, 'ajax.log')
        # f = open(fl, 'w')
        # f.write(str(e))
        # f.close()
        # x.script('notif("{0}", "error");'.format(e))
    x.script('stopLoad()')
    return x.json()

@dajaxice_register(method='GET')
def marcar_lida(request):
    x = Dajax()
    aluno = request.user.aluno
    notificacoes = NotificacoesAluno.objects.filter(para=aluno, lido=False)
    for notificacao in notificacoes:
        notificacao.lido = True
        notificacao.save()
    messages.info(request, '{0} Notificações marcadas como lidas.'.format(notificacoes.count()))
    x.script('window.location.reload();')
    return x.json()
