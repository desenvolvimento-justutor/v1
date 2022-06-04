# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17)
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: /home/tqi_cconceicao/PycharmProjects/justutor/app/justutor/omie/api.py
# Compiled at: 2022-05-06 04:38:28
import requests, json

APP_KEY = '2230484102847'
APP_SECRET = '1fa0ac7d8739b8c92439aea9442d7ed9'


class OmieAPI(object):

    def __init__(self, app_key=APP_KEY, app_secret=APP_SECRET):
        self._base_url = 'https://app.omie.com.br/api/v1/%s/'
        self.app_key = app_key
        self.app_secret = app_secret

    def request(self, endpoint, call, params):
        data = {'app_key': APP_KEY,
                'app_secret': APP_SECRET,
                'call': call,
                'param': [
                    params]}
        header = {'Content-type': 'application/json'}
        result = requests.post(url=self._base_url % endpoint, json=data, headers=header)
        if result.status_code != 200:
            raise Exception(json.dumps(result.json()['faultstring']))
        return json.dumps(result.json())

    def listar_cadastro_servico(self):
        result = self.request(endpoint='servicos/servico', call='ListarCadastroServico', params={'nPagina': 1,
                                                                                                 'nRegPorPagina': 20})
        return result

    def listar_clientes(self):
        result = self.request(endpoint='geral/clientes', call='ListarClientes', params={'pagina': 1,
                                                                                        'registros_por_pagina': 50,
                                                                                        'apenas_importado_api': 'N'})
        return result

    def incluir_cadastro_servico(self, descricao, codigo, preco_unit):
        params = {'intIncluir': {'cCodIntServ': codigo},
                  'descricao': {'cDescrCompleta': descricao},
                  'cabecalho': {'cDescricao': descricao,
                                'cCodigo': codigo,
                                'cIdTrib': '24',
                                'cCodServMun': '859960500',
                                'cCodLC116': '8.02',
                                'nIdNBS': '',
                                'nPrecoUnit': preco_unit,
                                'cCodCateg': '1.01.02'},
                  'impostos': {'nAliqISS': 0,
                               'cRetISS': 'N',
                               'nAliqPIS': 0,
                               'cRetPIS': 'N',
                               'nAliqCOFINS': 3,
                               'cRetCOFINS': 'S',
                               'nAliqCSLL': 2,
                               'cRetCSLL': 'S',
                               'nAliqIR': 1.5,
                               'cRetIR': 'S',
                               'nAliqINSS': 2,
                               'cRetINSS': 'S',
                               'nRedBaseINSS': 0}}
        result = self.request(endpoint='servicos/servico', call='IncluirCadastroServico', params=params)
        return result


if __name__ == '__main__':
    api = OmieAPI()
    print api.listar_clientes()
    print api.listar_cadastro_servico()
a = {'info': {'uInc': 'P000376770', 'dInc': '20/04/2022', 'hAlt': '09:16:44', 'hInc': '15:12:45', 'dAlt': '09/03/2022',
              'uAlt': 'P000376770',
              'inativo': 'N', 'cImpAPI': 'N'},
     'impostos': {'nAliqISS': 0,
                  'cRetISS': 'N',
                  'nAliqPIS': 0,
                  'cRetPIS': 'N',
                  'nAliqCOFINS': 3,
                  'cRetCOFINS': 'S',
                  'cRetIR': 'S',
                  'nAliqCSLL': 2,
                  'nAliqINSS': 2,
                  'cRetINSS': 'S',
                  'cRetCSLL': 'S',
                  'nRedBaseINSS': 0,
                  'nAliqIR': 1.5},
     'intListar': {'cCodIntServ': '', 'nCodServ': 2624899513},
     'descricao': {'cDescrCompleta': 'PR\\u00c1TICA DE SENTEN\\u00c7A/DISCURSIVAS ONLINE'},
     'cabecalho': {'cDescricao': 'PR\\u00c1TICA DE SENTEN\\u00c7A/DISCURSIVAS ONLINE', 'cCodigo': 'SRV00001',
                   'cCodCateg': '1.01.02',
                   'cCodServMun': '859960500', 'cIdTrib': '24', 'cCodLC116': '8.02', 'nIdNBS': '',
                   'nPrecoUnit': 0}}