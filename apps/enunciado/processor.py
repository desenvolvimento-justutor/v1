# -*- coding: utf-8 -*-
import logging
from django.utils import timezone
from .models import (EsferaGeral, TipoProcedimento, TipoPecaPratica, TipoPecaSentenca, Organizador,
                     Concurso, Disciplina, Localidade, OrgaoEntidade, Cargo, EsferaEspecifica,
                     AreaProfissional, EnunciadoProposta, Resposta, Correcao)
from apps.aluno.models import Aluno
logger = logging.getLogger(__name__)


def proc_enunciado(request):
    ret_dict = {
        'lista_anos': map(lambda x: {'id': x, 'name': str(x)}, range(2000, timezone.now().year+1)),
        'esfera_geral': EsferaGeral.objects.all(),
        'tipo_procedimento': TipoProcedimento.objects.all(),
        'tipo_peca_pratica': TipoPecaPratica.objects.all(),
        'tipo_peca_sentenca': TipoPecaSentenca.objects.all(),
        'organizador': Organizador.objects.all(),
        'concurso': Concurso.objects.all(),
        'disciplina': Disciplina.objects.all(),
        'localidade': Localidade.objects.all(),
        'orgao': OrgaoEntidade.objects.all(),
        'esfera_especifica': EsferaEspecifica.objects.all(),
        'cargo': Cargo.objects.all().order_by('nome'),
        'area_profissional': AreaProfissional.objects.all(),
        'total_peca': EnunciadoProposta.objects.filter(classificacao='PP').count(),
        'total_sentenca': EnunciadoProposta.objects.filter(classificacao='ST').count(),
        'total_questao': EnunciadoProposta.objects.filter(classificacao='QD').count(),
        'total_resposta': Resposta.objects.filter(ativo=True, concluido=True).count(),
        'total_correcao': Correcao.objects.filter().count(),
        'total_aluno': Aluno.objects.filter().count(),
    }
    return {'proc_enunciado': ret_dict}
