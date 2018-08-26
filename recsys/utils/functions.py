import requests
import json
import random

def getUsers():
    url = 'https://randomuser.me/api?nat=br&results=10&exc=location,dob,id,picture,gender'
    
    r = requests.get(url)

    response = r.json()

    return response


def gerarPessoa():
    """
    Gera dados de cadastro de uma pessoa, a partir da API do site 4Devs
    """

    pessoas = []

    url = 'https://www.4devs.com.br/ferramentas_online.php'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    sexo = ['H', 'M']

    for i in range(0, 10):
      

      payload = {
          'acao': 'gerar_pessoa',
          'sexo': random.choice(sexo),
          'idade': random.randrange(18, 100),
          'pontuacao': 'S',
          'cep_estado': 'CE',
          'cep_cidade': '1451'
      }

      r = requests.post(url, headers = headers, data= payload)

      response = r.json()

      dados = {
          "nome": response['nome'],
          "email": str(response['nome'].split(" ")[0].lower() + '@email.com'),
          "cpf": response['cpf'],
          "rg": response['rg'],
          "dt_nasc": response['data_nasc'],
          "telefone": response['telefone_fixo'],
          "celular": ''.join(c for c in response['celular'] if c not in '()- '),
      }

      pessoas.append(dados)
    

    return pessoas


pessoas = gerarPessoa()

for p in pessoas:
  print(p)

# for u in users["results"]:
#   print("Nome: {}; Email: {}; Username: {}; Senha: {}".format(
#     (u['name']['first'].capitalize() + " " + u['name']['last'].capitalize()),
#     u['email'],
#     (u['name']['first'] + u['name']['last']),
#     u['login']['password'],
    
#   ))