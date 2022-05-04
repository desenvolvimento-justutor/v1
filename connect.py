# -*- coding: utf-8 -*-
# Autor: christian

import os
import django
from django.db.models import Count, Q
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "justutorial.settings")
django.setup()


from apps.aluno.models import Aluno
from apps.enunciado.models import Resposta

r = Resposta.objects.get(id=441)
print r.aluno

# for x in a.get_seguidores:
#     print x.from_aluno, x.to_aluno