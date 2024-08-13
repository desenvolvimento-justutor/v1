# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from logging import getLogger
import html2text
import requests
from django.conf import settings

logger = getLogger("gpt")


class GPT:
    def __init__(
        self,
        modelo="gpt-4",
        max_tokens=600,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    ):
        self.api_key = settings.API_KEY_GPT
        # PARAMS
        self.modelo = modelo
        self.max_tokens = max_tokens
        self.temperature = float(temperature)
        self.top_p = float(top_p)
        self.frequency_penalty = float(frequency_penalty)
        self.presence_penalty = float(presence_penalty)

        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key),
        }
        self.gpt_result = None

    @staticmethod
    def gerar_prompt(
        enunciado,
        padrao_resposta,
        parametros_correcao,
        exemplos_correcao,
        resposta,
        instrucoes_gpt,
        instrucoes_recurso,
        optimize_tokens=True
    ):
        prompts_map = {
            "enunciado": enunciado,
            "padrao_resposta": padrao_resposta,
            "parametros_correcao": parametros_correcao,
            "exemplos_correcao": exemplos_correcao,
            "resposta": resposta,
            "instrucoes_gpt": instrucoes_gpt,
            "instrucoes_recurso": instrucoes_recurso,
        }

        prompts = []
        for key, value in prompts_map.iteritems():
            if not value:
                logger.debug("%s não informado: %r", *(key, value))
                continue
            if optimize_tokens:
                prompts.append(html2text.html2text(value))
            else:
                prompts.append(value)

        prompt = "\n\n".join(prompts)
        logger.debug("PROMPT \n%sprompt", prompt)
        return prompt

    def corrigir_resposta(self, prompt):
        data = {
            "model": self.modelo,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil que corrige respostas de alunos.",
                },
                {"role": "assistant", "content": prompt},
            ],
            "max_tokens": self.max_tokens,
            # "n": 1,
            # "stop": ["\n\n", "END"],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }
        logger.debug("CORRIGIR RESPOSTA: %s", data)
        # Enviando a requisição POST para a API da OpenAI
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        # Verificando a resposta e tratando erros
        if response.status_code == 200:
            result = response.json()
            logger.debug("GPT RESULT: %s", result)
            self.gpt_result = str(result)
            return result["choices"][0]["message"]["content"].strip()
        else:
            result = response.text
            logger.debug("GPT ERROR: %s", result)
            return result


if __name__ == "__main__":
    pass
