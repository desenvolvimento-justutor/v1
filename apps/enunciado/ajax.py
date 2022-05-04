# coding=utf-8
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
import re
from cepbr import CEP
from .models import ResponderDepois, EnunciadoProposta, AcompanharResposta, Coletania, Resposta, SeguirComentario, \
    CurtirComentario, RespostaComentario
from apps.aluno.models import aluno_from_user_request
from apps.website.utils import enviar_email

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
def seguir_resposta(request, rid):
    x = Dajax()
    try:
        aluno = aluno_from_user_request(request)
        if aluno:
            try:
                seguir = SeguirComentario.objects.get(aluno=aluno, resposta_id=rid)
                seguir.delete()
                x.script("swal('JusTutor', 'Você deixou de seguir esta resposta.', 'error')")
                x.script("$('#btnSeguir').removeClass('btn-warning').removeClass('btn-warning').addClass('btn-success')")
                x.script("""
                $('#btnSeguir').html('<i class="fa fa-bell-o"></i> Quero ser notificado dos comentários desta resposta')
                """)
            except SeguirComentario.DoesNotExist:
                seguir = SeguirComentario(aluno=aluno, resposta_id=rid)
                seguir.save()
                x.script("swal('JusTutor', 'Você começou a seguir esta resposta.', 'success')")
                x.script("$('#btnSeguir').removeClass('btn-success').addClass('btn-warning')")
                x.script("""
                $('#btnSeguir').html('<i class="fa fa-bell-slash-o"></i> Quero deixar de ser notificado dos comentários desta resposta')
                """)
        else:
            x.script("swal('Ops', 'Necessário efetuar login para adicionar o enunciado a sua lista', 'error')")
        x.script("$('#btnSeguir').attr('disabled', false)")
        x.script("$('#btnSeguir').removeClass('disabled')")
    except Exception as e:
        x.script("swal('Ops', '{}', 'error')".format(str(e)))
        x.script("$('#btnSeguir').button('reset')")
    return x.json()


@dajaxice_register(method='GET')
def responder_depois(request, eid):
    x = Dajax()
    aluno = aluno_from_user_request(request)
    enunciado = EnunciadoProposta.objects.get(id=eid)
    if aluno:
        rd = ResponderDepois.objects.filter(aluno=aluno, enunciado=enunciado)
        if rd:
            x.script("swal('', 'Enunciado {0} já adicionado a sua lista.', 'error')".format(enunciado))
        else:
            rd = ResponderDepois(aluno=aluno, enunciado=enunciado)
            rd.save()
            x.script("swal('', 'Enunciado {0} adicionado a sua lista.', 'success')".format(enunciado))
    else:
        x.script("swal('Ops', 'Necessário efetuar login para adicionar o enunciado a sua lista', 'error')")
    return x.json()


@dajaxice_register(method='GET')
def curtir_comentario(request, cid):
    x = Dajax()
    aluno = aluno_from_user_request(request)
    try:
        comentario = RespostaComentario.objects.get(id=cid)
        if aluno:
            if not CurtirComentario.objects.filter(comentario=comentario, aluno=aluno).first():
                x.script("swal('JusTutor', 'Você curtiu este comentário!.', 'success')")
                CurtirComentario(aluno=aluno, comentario=comentario).save()
                x.script("""$('#btnCurtir{}').html('<i class="fa fa-heart text-danger"></i>')""".format(cid))
            else:
                x.script("swal('JusTutor', 'Você já curtiu este comentário!.', 'error')")
            x.script("""$('#lblComentario{}').html('{}')""".format(cid, comentario.curtircomentario_set.all().count()))
        else:
            x.script("swal('Ops', 'Necessário efetuar login para comentar', 'error')")
        x.script("unBlockFunction()")
    except Exception as e:
        x.script("$('#btnCurtir{}').button('reset')".format(cid));
        x.script("swal('Ops', '{}', 'error')".format(str(e)))
        x.script("unBlockFunction()")
    return x.json()


@dajaxice_register(method='GET')
def adicionar_coletania(request, eid):
    x = Dajax()
    aluno = aluno_from_user_request(request)
    resposta = Resposta.objects.get(id=eid)
    if aluno:
        col = Coletania.objects.filter(aluno=aluno, resposta=resposta).first()
        if col:
            x.script("swal('Ops', 'Resposta {0} já adicionada à sua Coletânea.', 'error')".format(resposta))
            x.script("$('#btnColetania').button('reset')")
        else:
            col = Coletania(aluno=aluno, resposta=resposta)
            col.save()
            x.script("swal('\o/', 'Resposta {0} adicionada à sua Coletânea.', 'success')".format(resposta))
            x.script("""
            $('#tabResposta').html('RESPOSTA <i data-toggle="tooltip" data-original-title="Resposta adicionada à sua Coletânea" class="fa fa-star" style="color: #F89302; cursor: pointer"></i>')
            """)
            x.script("$('#btnColetania').tooltip('hide')")
            x.script("$('#btnColetania').hide()")
    else:
        x.script("swal('Ops', 'Necessário efetuar login para adicionar o enunciado a sua lista', 'error')")
        x.script("$('#btnColetania').button('reset')")
    return x.json()


@dajaxice_register(method='GET')
def acompanhar_resposta(request, eid):
    x = Dajax()
    aluno = aluno_from_user_request(request)
    enunciado = EnunciadoProposta.objects.get(id=eid)
    if aluno:
        rd = AcompanharResposta.objects.filter(aluno=aluno, enunciado=enunciado)
        if rd:
            x.script("swal('', 'Enunciado {0} já adicionado a sua lista.', 'error')".format(enunciado))
        else:
            rd = AcompanharResposta(aluno=aluno, enunciado=enunciado)
            rd.save()
            x.script("swal('', 'Enunciado {0} adicionado a sua lista.', 'success')".format(enunciado))
    else:
        x.script("swal('Ops', 'Necessário efetuar login para adicionar o enunciado a sua lista', 'error')")
    return x.json()


@dajaxice_register(method='GET')
def acompanhar_remover(request, eid):
    x = Dajax()
    rd = AcompanharResposta.objects.get(id=eid)
    enunciado = rd.enunciado
    rd.delete()
    x.script('$("#acompanhar-{0}").hide("slow");'.format(eid))
    x.script(u'_toastr("Você deixou de acompanhar o Enunciado {0}","top-right","success",false);'.format(enunciado))
    return x.json()


@dajaxice_register(method='GET')
def relatar_bug(request, tipo, url, msg):
    x = Dajax()
    aluno = aluno_from_user_request(request)
    ctx = {
        'aluno': aluno,
        'url': url,
        'tipo': tipo,
        'mensagem': msg
    }
    enviar_email('email/reportar-bug.html', u'Erro relatado ({0})'.format(tipo),
                 ['conteudo@justutor.com.br', 'cristiane@justutor.com.br'], ctx, ead=True)
    x.script("swal_alert('Obrigado', 'O problema foi reportado e iremos efetuar a análise!', 'success');")
    return x.json()



