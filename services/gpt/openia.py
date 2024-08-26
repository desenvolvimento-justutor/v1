# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
import html2text
import requests
from logging import getLogger
from django.conf import settings

logger = getLogger("gpt")


def formatar_texto(texto):
    texto = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"\n+", "<br>", texto)
    return texto


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
        optimize_tokens=True,
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

        prompts = [
            html2text.html2text(value) if optimize_tokens else value
            for key, value in prompts_map.iteritems()
            if value
        ]

        prompt = "\n\n".join(prompts)
        logger.debug("Generated prompt: \n%s", prompt)
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
                # {"role": "user", "content": "Por favor, formate a resposta como HTML."},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }
        logger.debug("Request data: %s", data)

        try:
            response = requests.post(
                self.url, headers=self.headers, data=json.dumps(data)
            )
            logger.debug("GPT Response: %s", response.json())
            response.raise_for_status()  # Levanta um erro se o status for >= 400
            result = response.json()
            logger.debug("GPT result: %s", result)
            self.gpt_result = result
            content = result["choices"][0]["message"]["content"].strip()
            return formatar_texto(content)
        except requests.exceptions.RequestException as e:
            logger.error("Error in GPT API request: %s", e)
            return None
