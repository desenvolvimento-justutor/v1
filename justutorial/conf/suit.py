# -*- coding: utf-8 -*-
# Autor: christian

FILEBROWSER_SUIT_TEMPLATE = True
SUIT_CONFIG = {
    'ADMIN_NAME': 'JusTutorial',
    'HEADER_DATE_FORMAT': 'D. j \d\e F \d\e Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'MENU': (
        # Rename app and set icon
        # Reorder app models
        'sites',
        'social_auth',
        'django_comments',
        'threadedcomments',
        {'label': u'Segurança',
         'icon': 'icon-lock',
         'models': (
             'auth.user',
             'auth.group'
         )},
        {'label': u'Textos & Artigos',
         'icon': 'icon-lock',
         'models': (
             'website.artigoindice',
             'website.artigo'
         )},
        {'label': u'Website',
         'icon': 'icon-globe',
         'models': (
             'website.configuracao',
             'website.institucional',
             'website.banner',
             'website.videojustutor',
             'website.noticia',
             'website.anuncio'
         )},
        {'label': 'PagSeguro',
         'icon': 'icon-shopping-cart',
         'models': (
             'pagseguro.checkout',
             'pagseguro.transaction',
             'curso.checkoutitens'
         )},
        {'label': u'Área do Aluno',
         'icon': 'icon-user',
         'models': (
             'aluno.aluno',
             'enunciado.resposta',
             'enunciado.correcao',
         )},
        {'label': u'Bolsa de Correção',
         'icon': 'icon-user',
         'models': (
             'corretor.corretor',
         )},
        {'label': u'Cursos',
         'icon': 'icon-certificate',
         'models': (
             'curso.categoria',
             'curso.curso',
             'curso.atividade',
             'curso.tarefaatividade',
             'curso.modulo',
             'curso.destaque',
             'curso.serie',
             'curso.cursogratis',
         )},
        {'label': u'Promoções',
         'icon': 'icon-certificate',
         'models': (
             'enunciado.rankingpremiado',
         )},
        {'label': u'Corretor',
         'icon': 'icon-certificate',
         'models': (
             'corretor.Corretor',
         )},
        {'label': u'Cadastro',
         'icon': 'icon-edit',
         'models': (
             'enunciado.esferageral',
             'enunciado.esferaespecifica',
             'enunciado.cargo',
             'enunciado.areaprofissional',
             'enunciado.orgaoentidade',
             'enunciado.tipoprocedimento',
             'enunciado.tipopecapratica',
             'enunciado.tipopecasentenca',
             'enunciado.organizador',
             'enunciado.localidade',
             'enunciado.disciplina',
             'enunciado.concurso',
             'enunciado.tag',
             'professor.professor'
         )},
        {'label': 'Enunciado',
         'icon': 'icon-list-alt',
         'models': (
             'enunciado.enunciadopropostasentenca',
             'enunciado.enunciadopropostapratica',
             'enunciado.enunciadopropostadiscursiva',
         )},
    )
}
