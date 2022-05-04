# -*- coding: utf-8 -*-
# Autor: christian

from django.db.models import Q
from models import Curso, Categoria, Serie
from django.utils import timezone
from carton.cart import Cart


def proc_curso(request):
    now = timezone.now()
    cursos = Curso.objects.filter(Q(data_ini__lte=now), Q(data_fim__gte=now) | Q(data_fim=None))
    cart = Cart(request.session)
    cart.update_session()
    ret = {
        'cursos': cursos,
        'categorias': Categoria.objects.filter(tipo__in=['C', 'B']),
        'sentencas_avulsas': Categoria.objects.filter(tipo='S'),
        'sentencas_oab': Categoria.objects.filter(tipo='O'),
        'livraria': Categoria.objects.filter(tipo='L'),
        'combo': Categoria.objects.filter(tipo='B'),
        'simulados': Categoria.objects.filter(tipo='D'),
        'series': Serie.objects.all(),
        'cart': cart
    }
    return {'proc_curso': ret}
