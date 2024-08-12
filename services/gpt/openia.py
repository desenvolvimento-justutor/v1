# -*- coding: utf-8 -*-
import json

import html2text
import requests
from django.conf import settings


class GPT:
    def __init__(self, modelo="gpt-4", max_tokens=600, temperature=0.5, top_p=0.9):
        self.api_key = settings.API_KEY_GPT
        # PARAMS
        self.modelo = modelo
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key),
        }

    def gerar_prompt(
        self,
        enunciado,
        padrao_resposta,
        frases_de_correcao,
        instrucoes_adicionais,
        resposta_aluno,
        exemplos_de_correcao=None,
    ):

        prompt = "{enunciado}\n\nResposta do aluno:\n{resposta_aluno}\n\n{padrao_resposta}\n".format(
            enunciado=enunciado.encode("utf-8"),
            resposta_aluno=resposta_aluno.encode("utf-8"),
            padrao_resposta=padrao_resposta.encode("utf-8"),
        )

        if exemplos_de_correcao:
            prompt += "\n{}\n".format(exemplos_de_correcao.encode("utf-8"))
        prompt += "\n{}\n\n{}\n\nCorreção do JusTutor:".format(
            frases_de_correcao.encode("utf-8"), instrucoes_adicionais.encode("utf-8")
        )

        return prompt

    @staticmethod
    def _html2text(html):
        return html2text.html2text(html)

    def corrigir_resposta(self, prompt):
        data = {
            "model": self.modelo,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil que corrige respostas de alunos.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 600,
            "n": 1,
            "stop": ["\n\n", "END"],
            "temperature": 0.5,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
        }

        # Enviando a requisição POST para a API da OpenAI
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        # Verificando a resposta e tratando erros
        if response.status_code == 200:
            result = response.json()
            print("*" * 100)
            print(result)
            print("*" * 100)
            return result["choices"][0]["message"]["content"].strip()
        else:
            print("Erro:", response.status_code)
            print(response.text)
            return None


if __name__ == "__main__":
    pass
