# -*- coding: utf-8 -*-

import openai

# Defina sua chave de API da OpenAI

openai.api_key = None


# Função para gerar o prompt
def gerar_prompt(resposta_aluno, exemplos_de_correcao=None):
    enunciado = """
    ENUNCIADO DA QUESTÃO:
    João e Maria, pais de Ana, uma criança de 5 anos, se divorciaram recentemente. Maria ficou com a guarda de Ana e, devido a dificuldades financeiras, não consegue suprir todas as necessidades da filha. Mesmo após diversas tentativas, Maria não conseguiu que João contribuísse financeiramente para o sustento de Ana. Diante dessa situação, o Ministério Público ajuizou uma ação de alimentos em favor de Ana.
    1. O fato de haver, na localidade, uma Defensoria Pública cuja atuação seja eficiente, bem como de Ana não estar em uma situação de risco, interfere na legitimidade do Ministério Público para ajuizar a ação de alimentos em favor da criança? Explique.
    2. Em quais situações a atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos? Dê três exemplos específicos.
    """

    padrao_resposta = """
    PADRÃO DE RESPOSTA:
    1. O fato de haver, na localidade, uma Defensoria Pública atuando de forma eficiente, bem como de Ana não estar em uma situação de risco, não interfere na legitimidade do Ministério Público para ajuizar a ação de alimentos em favor da criança (Q01). Isso porque o direito à alimentação é considerado indisponível e de extrema relevância social, conferindo legitimidade ao MP para promover ações de alimentos, independentemente da atuação da Defensoria Pública ou da situação de risco (Q02).
    2. A atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos em situações como: (i) quando os responsáveis legais não têm condições financeiras para arcar com os custos de uma ação judicial; (ii) quando há conflito de interesses entre o menor e seus responsáveis; (iii) quando a Defensoria Pública não está presente ou não pode atuar de forma eficaz (Q03).
    """

    frases_de_correcao = """
    Frases de Correção:
    QUESITO 01. LEGITIMIDADE DO MINISTÉRIO PÚBLICO (0,60 PONTO)
    - Respondeu corretamente que o fato de haver, na localidade, uma Defensoria Pública atuando de forma eficiente, bem como de Ana não estar em uma situação de risco, não interfere na legitimidade do Ministério Público para ajuizar a ação de alimentos em favor da criança. (NOTA INTEGRAL)
    - A resposta não abordou o tema tratado neste item da correção. (- 0,60)
    - A resposta está totalmente incorreta, pois disse que a presença da Defensoria Pública eficiente e a ausência de risco para Ana interferem na legitimidade do Ministério Público para ajuizar a ação de alimentos. (- 0,60)

    QUESITO 02. FUNDAMENTO DA LEGITIMIDADE DO MINISTÉRIO PÚBLICO (0,60 PONTO)
    - Respondeu corretamente que o direito à alimentação é considerado indisponível e de extrema relevância social, conferindo legitimidade ao MP para promover ações de alimentos, independentemente da atuação da Defensoria Pública ou da situação de risco. (NOTA INTEGRAL)
    - A resposta não abordou o tema tratado neste item da correção. (- 0,60)
    - A resposta está totalmente incorreta, pois não mencionou que o direito à alimentação é considerado indisponível e de extrema relevância social, conferindo legitimidade ao MP para promover ações de alimentos. (- 0,60)

    QUESITO 03. SITUAÇÕES EM QUE A ATUAÇÃO DO MP É FUNDAMENTAL (0,80 PONTO)
    - Apresentou três exemplos corretos de situações em que a atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (NOTA INTEGRAL)
    - A resposta não abordou o tema tratado neste item da correção. (- 0,80)
    - A resposta está totalmente incorreta, pois não mencionou nenhuma situação em que a atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,80)
    - A resposta não mencionou um dos exemplos específicos em que a atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,27)
    - A resposta não mencionou dois dos exemplos específicos em que a atuação do Ministério Público é fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,53)
    - A resposta apresentou um exemplo incorreto, que não expressa uma situação em que a atuação do Ministério Público seja fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,27)
    - A resposta apresentou dois exemplos incorretos, que não expressam situações em que a atuação do Ministério Público seja fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,53)
    - A resposta apresentou três exemplos incorretos, que não expressam situações em que a atuação do Ministério Público seja fundamental na proteção dos direitos de crianças e adolescentes em ações de alimentos. (- 0,80)
    """

    instrucoes_adicionais = """
    Com base na resposta apresentada, selecione a frase de correção mais apropriada para cada quesito. Se a resposta não se encaixar exatamente em uma das frases, adicione um comentário adicional.
    """

    prompt = (
        "{enunciado}\n\nResposta do aluno:\n{resposta_aluno}\n\n{padrao_resposta}\n".format(
            enunciado=enunciado, resposta_aluno=resposta_aluno, padrao_resposta=padrao_resposta
        )
    )

    if exemplos_de_correcao:
        prompt += "\n{}\n".format(exemplos_de_correcao)
    prompt += "\n{}\n\n{}\n\nCorreção do JusTutor:".format(frases_de_correcao, instrucoes_adicionais)

    return prompt


# Função para corrigir a resposta do aluno usando um modelo específico


def corrigir_resposta(resposta_aluno, exemplos_de_correcao=None, modelo="gpt-3"):
    prompt = gerar_prompt(resposta_aluno, exemplos_de_correcao)
    response = openai.Completion.create(
        model=modelo,  # Especifica o modelo aqui
        prompt=prompt,
        max_tokens=600,
        n=1,
        stop=[
            "\n\n",
            "END",
        ],  # Adiciona stop sequences para controlar onde parar a geração de texto
        temperature=0.5,
        top_p=0.9,  # Ajuste do top_p para controlar a aleatoriedade
        frequency_penalty=0.5,  # Ajuste do frequency_penalty para controlar a repetição
    )
    return response.choices[0].text.strip()


if __name__ == "__main__":
    resposta = """<p>Na hip&oacute;tese de existir, na localidade, &oacute;rg&atilde;o da Defensoria P&uacute;blica com atua&ccedil;&atilde;o eficiente, tal situa&ccedil;&atilde;o n&atilde;o interfere na legitimidade do Minist&eacute;rio P&uacute;blico ajuizar a&ccedil;&atilde;o de alimentos, haja vista que a atua&ccedil;&atilde;o de tais &oacute;rg&atilde;os n&atilde;o se confunde.</p>

<p>O Minist&eacute;rio P&uacute;blico atuar&aacute; como substituto processual, em nome pr&oacute;rpio, inclusive de of&iacute;cio,&nbsp;na defesa de Ana aos alimentos. Por outro lado, a Defensoria P&uacute;blica atuar&aacute; como representante processual, pleiteando em nome de Ana, os alimentos.&nbsp;</p>

<p>Ainda,&nbsp;insta destacar que o Minist&eacute;rio P&uacute;blico poder&aacute; propor a&ccedil;&atilde;o de alimentos mesmo que Ana n&atilde;o esteja em situa&ccedil;&atilde;o de risco, tendo em vista o princ&iacute;pio da prote&ccedil;&atilde;o integral e da interven&ccedil;&atilde;o precoce,&nbsp;segundo o qual a atua&ccedil;&atilde;o do Estado na prote&ccedil;&atilde;o da crian&ccedil;a deve suceder antes que esteja em situa&ccedil;&atilde;o irregular.</p>

<p>Outrossim, o&nbsp;Minist&eacute;rio P&uacute;blico poder&aacute; atuar na prote&ccedil;&atilde;o dos direitos das crian&ccedil;as e adolescentes, notadamente na propositura de a&ccedil;&atilde;o de alimentos, de destitui&ccedil;&atilde;o e suspens&atilde;o do poder familiar, assim como de nomea&ccedil;&atilde;o e remo&ccedil;&atilde;o de tutores, curadores e guardi&atilde;es.</p>
"""
    exemplos_de_correcao = (
        None  # Ou a string de exemplos de correção, se disponíveis
    )
    correcao = corrigir_resposta(resposta, exemplos_de_correcao)
