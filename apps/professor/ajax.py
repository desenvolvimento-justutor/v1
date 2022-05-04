# coding=utf-8
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from .models import Mensagem
from apps.website.utils import enviar_email
from apps.professor.models import Professor
from apps.curso.models import Curso
from apps.aluno.models import Aluno


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
    x.script('_toastr("Mensagem marcada como Visualizada.","top-right","success",false);')
    x.script('stopLoad()')
    return x.json()


@dajaxice_register(method='GET')
def enviar_mensagem(request, pid, mensagem, cid, tp='A'):
    x = Dajax()
    try:
        args = {
            'mensagem': mensagem,
            'professor': request.user.professor if tp == 'P' else None
        }
        if cid in ['sentenca', 'st']:
            args['sentenca'] = True
        elif cid == 'oab':
            args['oab'] = True
        else:
            args['curso_id'] = cid

        if tp == 'P':  # Mensagem do professor para o aluno
            args.update({
                'resposta': True,
                'aluno_id': pid,
            })
        else:  # Mensagem do aluno para o professor
            args.pop('professor')
            args.update({
                'aluno': request.user.aluno,
                'professor_id': pid
            })
        msg = Mensagem(**args)
        msg.save()
        x.script('_toastr("Sua mensagem foi enviada.","top-right","success",false);')

        vl = {'sentenca': "Atividades Avulsas", 'st': "Atividades Avulsas", 'oab': "OAB 2ª Fase"}
        vlt = {'sentenca': "st", 'st': "st", 'oab': "oab"}
        ctx = {}
        if cid in ['sentenca', 'st', 'oab']:
            ctx['curso'] = vl.get(cid)
            ctx['tipo'] = vlt.get(cid)
        else:
            obj_curso = Curso.objects.get(id=cid)
            ctx['curso'] = obj_curso.nome
            ctx['cid'] = cid

        if tp == 'P':
            x.script('$(".btn-success[data-aid=%s]").click()' % pid)
            obj_professor = request.user.professor
            obj_aluno = Aluno.objects.get(pk=pid)
            ctx.update({
                'professor': obj_professor,
                'mensagem': mensagem
            })
            enviar_email('professor/email/nova-mensagem.html', 'Nova mensagem', [obj_aluno.usuario.email],
                         ctx, ead=True)
        else:
            x.script('$(".btn-success[data-pid=%s]").click()' % pid)
            obj_professor = Professor.objects.get(pk=pid)
            obj_aluno = request.user.aluno
            ctx.update({
                'aluno': obj_aluno,
                'mensagem': mensagem,
                'tipo_url': 2

            })
            enviar_email('professor/email/nova-mensagem.html', 'Nova mensagem', [obj_professor.user.email],
                         ctx, ead=True)
    except Exception as e:
        x.script('notif("{0}", "error");'.format(e))

    x.script('stopLoad()')
    # x.script('''$( "[data-name='ver']" ).click();''')
    return x.json()


@dajaxice_register(method='GET')
def enviar_mensagem_sentenca(request, pid, mensagem):
    x = Dajax()
    try:
        args = {
            'mensagem': mensagem,
            'aluno': request.user.aluno,
            'professor_id': pid,
            'sentenca': True
        }

        msg = Mensagem(**args)
        msg.save()
        x.script('_toastr("Sua mensagem foi enviada.","top-right","success",false);')
    except Exception as e:
        x.script('notif("{0}", "error");'.format(e))

    x.script('stopLoad()')
    x.script('''$( "[data-name='ver']" ).click();''')
    return x.json()
