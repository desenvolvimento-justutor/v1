import json

from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from .models import ConfiguracaoPacote


def teste(request):
    return render(request, 'financeiro/financeiro.html')


def get_credito(request):
    config = ConfiguracaoPacote.objects.filter(ativo=True).first()
    print '***', config
    data = {
        'config': model_to_dict(config),
        'descontos': json.loads(serializers.serialize('json', config.descontos.all())),
        'pacotes': json.loads(serializers.serialize('json', config.pacotes.all())),
    }
    return JsonResponse(data)
