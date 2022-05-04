# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.text import mark_safe
from django import template
from apps.curso.models import Curso, CursoGratis
from apps.website.models import Noticia, Banner
from django.utils import timezone
from django.db.models import Q

register = template.Library()


@register.simple_tag
def tooltip(title, placement='bottom'):
    """
    :param title:
    :param placement: left, bottom, top, right
    :return:
    """
    fmt = 'data-container="body" data-toggle="tooltip"' \
          ' data-placement="{placement:s}" data-original-title="{title:s}"'
    return mark_safe(
        fmt.format(placement=placement, title=title)
    )


@register.simple_tag
def cursos_recentes():
    ret = []
    now = timezone.now()
    args = [
        Q(data_ini__lte=now), Q(data_fim__gte=now) | Q(data_fim=None)
    ]

    # CURSOS
    cursos = Curso.objects.filter(categoria__tipo__in=['C', 'B'], *args).order_by('-data_ini')[:6]
    cursos_count = cursos.count()
    if cursos_count:
        ret.append({
            'categoria': 'Cursos',
            'destaque': cursos[0] if cursos_count > 1 else False,
            'cursos': cursos,
            'total': cursos_count,
            'bg': 'lifestyle',
            'img': 'website/images/site/cursos.jpg'
        })

    # CURSOS GRATIS
    cursos_gratis = CursoGratis.objects.all()[:6]
    cursos_gratis_count = cursos_gratis.count()
    if cursos_gratis_count:
        ret.append({
            'categoria': 'Cursos Grátis',
            'destaque': cursos_gratis[0] if cursos_gratis_count > 1 else False,
            'cursos': cursos_gratis,
            'total': cursos_gratis_count,
            'bg': 'food',
            'img': 'website/images/site/cursos-gratis.jpg'
        })

    # SENTENCAS AVULSAS
    cursos_sentenca = Curso.objects.filter(categoria__tipo='S', *args).order_by('-data_ini')[:6]
    cursos_sentenca_count = cursos_sentenca.count()
    if cursos_sentenca_count:
        ret.append({
            'categoria': 'Atividades Avulsas',
            'destaque': cursos_sentenca[0] if cursos_sentenca_count > 1 else False,
            'cursos': cursos_sentenca,
            'total': cursos_sentenca_count,
            'bg': 'market',
            'img': 'website/images/site/cursos.jpg'
        })
    return ret


@register.simple_tag
def noticias_recentes(count=5):
    now = timezone.now()
    noticias = Noticia.objects.filter(
        Q(ativo_inicio__lte=now),
        Q(ativo_fim__gte=now) | Q(ativo_fim=None)
    ).order_by('-ativo_inicio')[:count]
    return noticias


def get_banners():
    now = timezone.now()
    banners = Banner.objects.filter(
        Q(ativo_inicio__lte=now),
        Q(ativo_fim__gte=now) | Q(ativo_fim=None)
    ).order_by('-ativo_inicio')
    return banners


@register.inclusion_tag('frotend/tags/slider1.html')
def slider1():
    return {
        'banners': get_banners()
    }


@register.inclusion_tag('frotend/tags/slider/revolution.html')
def render_slider_revolution():
    return {
        'banners': get_banners()
    }
