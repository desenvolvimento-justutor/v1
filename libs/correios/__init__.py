# coding=utf-8
from pprint import pprint
from urllib import urlencode
from xml.dom import minidom
import urllib2

class Frete(object):
    _url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
    url = ''
    params = {}
    result = ''
    xfactor = 1
    codes = {'81019':'E-Sedex', '41106':'PAC', '40010':'Sedex', '40215': 'Sedex 10', '41017':'Normal', '40045':'Sedex a cobrar', '44105':'OTE', '40290':'Sedex hoje'}
    def __init__(self, nCdServico, sCepOrigem, sCepDestino, nVlPeso, nVlComprimento, nVlAltura, nVlLargura, sCdMaoPropria=0, nVlValorDeclarado=0, sCdAvisoRecebimento=0, nVlDiametro=0, nCdEmpresa='', sDsSenha='', nCdFormato=1):
        tipos = nCdServico.split(',')
        x = [x for x in tipos if x in self.codes]
        nCdServico = ','.join(x)
        self.params = {
            'nCdServico': nCdServico,
            'sCepOrigem': sCepOrigem,
            'sCepDestino': sCepDestino,
            'nVlPeso': int(nVlPeso),
            'nVlComprimento': int(nVlComprimento),
            'nVlAltura': int(nVlAltura),
            'nVlLargura': int(nVlLargura),
            'nCdEmpresa':nCdEmpresa,
            'sDsSenha':sDsSenha,
            'nCdFormato':nCdFormato,
            'sCdMaoPropria':sCdMaoPropria,
            'nVlValorDeclarado':nVlValorDeclarado,
            'sCdAvisoRecebimento':sCdAvisoRecebimento,
            'nVlDiametro':nVlDiametro,
            'StrRetorno': 'xml'
        }

    def get(self):
        self.set_min_dimensions()
        self.set_max_dimensions()
        self.set_url()
        self.set_result()
        return self.get_result_object()

    def set_url(self):self.url = '%s?%s' % (self._url, urlencode(self.params))

    def set_min_dimensions(self):
        if int(self.params['nVlComprimento']) < 16: self.params['nVlComprimento'] = 16
        if int(self.params['nVlLargura']) < 11: self.params['nVlLargura'] = 11
        if int(self.params['nVlAltura']) < 2: self.params['nVlAltura'] = 2

    def set_max_dimensions(self):
        soma = int(self.params['nVlComprimento']) + int(self.params['nVlLargura']) + int(self.params['nVlAltura'])
        if int(self.params['nVlComprimento']) > 105: self.params['nVlComprimento'] = 105
        if int(self.params['nVlLargura']) > 105: self.params['nVlLargura'] = 105
        if int(self.params['nVlAltura']) > 105: self.params['nVlAltura'] = 105
        nsoma = int(self.params['nVlComprimento']) + int(self.params['nVlLargura']) + int(self.params['nVlAltura'])
        if nsoma > 200:
            dif = nsoma - 200
            if int(self.params['nVlLargura']) - dif > 11:
                self.params['nVlLargura'] = int(self.params['nVlLargura']) - dif
            elif int(self.params['nVlComprimento']) - dif > 16:
                self.params['nVlComprimento'] = int(self.params['nVlComprimento']) - dif
            elif int(self.params['nVlAltura']) - dif > 2:
                self.params['nVlAltura'] = int(self.params['nVlAltura']) - dif
            else:
                self.params['nVlLargura'] = 66
                self.params['nVlComprimento'] = 66
                self.params['nVlAltura'] = 66
        if soma > 200: self.xfactor = float(soma) / 200
        if self.params['nVlPeso'] > 30:
            pesofactor = self.params['nVlPeso'] / 30
            self.params['nVlPeso'] = 30
            if pesofactor > self.xfactor:
                self.xfactor = pesofactor

    def set_result(self): self.result = minidom.parse(urllib2.urlopen(self.url))

    def get_result_object(self):
        tags_name = ('MsgErro', 'Erro', 'Codigo', 'Valor', 'PrazoEntrega', 'ValorMaoPropria', 'ValorValorDeclarado', 'EntregaDomiciliar', 'EntregaSabado',)
        servicos, dados = {}, {}

        for servico in self.result.getElementsByTagName('cServico'):
            for tag_name in tags_name:
                try: dados[tag_name] = servico.getElementsByTagName(tag_name)[0].childNodes[0].data
                except: dados[tag_name] = ''
                try: dados['nome'] = self.codes[servico.getElementsByTagName('Codigo')[0].childNodes[0].data]
                except: pass
            servicos[servico.getElementsByTagName('Codigo')[0].childNodes[0].data] = dados
            dados = {}
        for servico in servicos:
            valor = float(servicos[servico]['Valor'].replace('.','').replace(',','.'))
            servicos[servico]['Valor'] = valor * self.xfactor
        return servicos