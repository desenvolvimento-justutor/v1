# -*- coding: utf-8 -*-

import json
import os
import uuid
import requests

ROOT_DIR = os.path.dirname(__file__)

PEM_FILE = os.path.join(ROOT_DIR, "cert/Justutor_Prod.pem")
KEY_FILE = os.path.join(ROOT_DIR, "cert/Justutor_Prod.key")
CLIENT_KEY = "42017530-8b9c-11ed-a1eb-0242ac120002"

BASE_URL = "https://secure.api.pagseguro.com"


# response = requests.request("POST", url, headers=headers, data=payload, cert=cert)
#
# print(response.text)


class ApiPIX:
    def request(self, method, endpoint, payload={}, headers={}, token=None):
        _headers = {
            'Authorization': 'Basic NDIwMTc1MzAtOGI5Yy0xMWVkLWExZWItMDI0MmFjMTIwMDAyOjQyMDE3ODBhLThiOWMtMTFlZC1hMWViLTAyNDJhYzEyMDAwMg==',
            'Content-Type': 'application/json'
        }
        url = BASE_URL + endpoint
        cert = (PEM_FILE, KEY_FILE)
        if token:
            _headers.update({
                "Authorization": "Bearer %s" % token
            })
        response = requests.request(method, url, headers=_headers, data=payload, cert=cert)
        if not response.status_code in [200, 201]:
            raise Exception(response.json())
        return response

    def get_token(self):
        payload = json.dumps({
            "grant_type": "client_credentials",
            "scope": "cob.read cob.write payloadlocation.read payloadlocation.write pix.read pix.write webhook.read webhook.write"
        })
        response = self.request("POST", "/pix/oauth2", payload)
        return response.json()["access_token"]

    def get_cob(self, txid):
        token = self.get_token()
        url = "/instant-payments/cob/%s?revisao=0" % txid
        response = self.request("GET", url, token=token)
        return response.json()

    def create_cob(self, cpf, nome, valor):
        txid = uuid.uuid4().hex
        token = self.get_token()
        url = "/instant-payments/cob/%s" % txid
        payload = json.dumps({
            "calendario": {
                "expiracao": "3600"
            },
            "devedor": {
                "cpf": "%s" % cpf,
                "nome": "%s" % nome
            },
            "valor": {
                "original": "%.2f" % valor
            },
            "chave": "24181548000143",
            "solicitacaoPagador": "Serviço realizado.",
            "infoAdicionais": [
                {
                    "nome": "Serviço",
                    "valor": "Serviços Justutor"
                }
            ]
        })
        response = self.request("PUT", url, payload=payload, token=token)
        return response.json()

    def create_webhook(self):
        token = self.get_token()
        url = "/instant-payments/webhook/24181548000143"
        payload = json.dumps({
            "webhookUrl": "https://justutor.com.br/pagseguro/pix",
        })
        response = self.request("PUT", url, payload=payload, token=token)
        return response.text

    def get_webhook(self):
        token = self.get_token()
        url = "/instant-payments/webhook/24181548000143"
        response = self.request("GET", url, token=token)
        return response.json()


if __name__ == "__main__":
    api = ApiPIX()
    a = api.get_webhook()
