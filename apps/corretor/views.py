# -*- coding: utf-8 -*-
# Autor: christian
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .forms import FormCorretor
from apps.website.utils import enviar_email
from apps.pregao.models import SolicitarCorrecao
from django.db.models import Q


def corretor_required(user):
    try:
        user.corretor
    except:
        raise PermissionDenied('Área restrita a professores')
    return user


@login_required
@user_passes_test(corretor_required)
def painel(request):
    context = {
        'menu': 'painel',
        'titulo': 'Painel'
    }
    return render(request, 'corretor/painel.html', context)


@login_required
@user_passes_test(corretor_required)
def pregao(request):
    args = [Q(status="E")]
    filtro = request.GET.get('filtro')
    if filtro == 'corretor':
        corretor = request.user.corretor
        args.append(Q(corretores=corretor))
    osolicitacoes = SolicitarCorrecao.objects.filter(*args)

    context = {
        'menu': 'pregao',
        'titulo': 'Pregão',
        'filtro': filtro,
        'solicitacoes': osolicitacoes
    }
    return render(request, 'corretor/pregao.html', context)


def cadastro(request):
    if request.method == 'POST':
        form = FormCorretor(request.POST)
        if form.is_valid():
            corretor = form.save()
            context = {
                'titulo': 'Cadastro prévio enviado!',
                'mensagem': 'Nossa equipe vai analisar seus dados e você receberá nosso contato em breve'
            }

            enviar_email(
                'corretor/email/cadastro-efetuado.html',
                u'Pré cadastro de corretor',
                ['christian.douglas.alcantara@gmail.com', 'conteudo@justutor.com.br'], {'corretor': corretor}
            )

            return render(request, 'corretor/mensagem.html', context)
    else:
        form = FormCorretor()

    context = {
        'form': form
    }
    return render(request, 'corretor/form-cadastro.html', context)