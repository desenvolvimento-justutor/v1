from collections import OrderedDict

if __name__ == "__main__":
    sender = {
        'name': "data['name_on_card'] or data['nome'] or request.user.aluno",
        'area_code': "ddd",
        'phone': "phone",
        'email': "data['email']",
        'cpf': "re.sub('[^0-9]', '', data['cpf']"
    }
    # SHIPPING
    shipping = {
        'street': "data['logradouro']",
        'number': "data['numero']",
        'complement': "data['complemento']",
        'district': "data['bairro']",
        'postal_code': "re.sub('[^0-9]', '', data['cep'])",
        'city': "data['cidade']",
        'state': "data['uf']",
        'country': 'BRA'
    }

    info_d = OrderedDict(sender)
    info_d.update(shipping)
    info = "Nome       : {name}\n" \
           "CPF        : {cpf}\n" \
           "DDD        : {area_code}\n" \
           "Fone       : {phone}\n" \
           "E-Mail     : {email}\n" \
           "Endereco   : {street}\n" \
           "Numero     : {number}\n" \
           "Complemento: {complement}\n" \
           "Bairro     : {district}\n" \
           "Cidade     : {city}\n" \
           "UF         : {state}\n" \
           "CEP        : {postal_code}".format(**info_d)
    print info
