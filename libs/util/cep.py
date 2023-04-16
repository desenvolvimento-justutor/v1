import json
import requests
import re


class ViaCEP:

    def __init__(self, cep):
        self.cep = cep

    def getDadosCEP(self):
        url_api = ('http://www.viacep.com.br/ws/%s/json' % self.cep)
        req = requests.get(url_api)
        if req.status_code == 200:
            dados_json = json.loads(req.text)
            return dados_json


def get_cep(cep):
    cep = re.sub("[-/.]", "", cep)
    d = ViaCEP(cep)
    data = d.getDadosCEP()
    return data


if __name__ == "__main__":
    print get_cep("77813540")