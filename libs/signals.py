# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
from django.utils import timezone

def create_slug(sender, instance, signal, *args, **kwargs):
    # check for id and attributes
    if instance.id:
        # get slug information
        slug_name = 'slug'
        slug_from = 'nome'
        # save slug if empty
        if not getattr(instance, slug_name, None):
            # create slug
            slug = u'{0:s}-{1}'.format(slugify(getattr(instance, slug_from)), instance.id)
            # set slug
            setattr(instance, slug_name, slug)
            # save instance
            instance.save()


def tarefa_atividade_save(sender, instance, signal, *args, **kwargs):
    # check for id and attributes
    if instance.concluido:
        instance.data_conclusao = timezone.now()