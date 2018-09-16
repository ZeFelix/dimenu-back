from django.conf import settings
import requests
import json
import random
import redis
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from api.models import Client, Avaliation, Product, Company
from recsys.recommender import svd
import pandas as pd

redisInstance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


def setDataInRedis(companyID):
    preds, products, ratings = svd.loadData(companyID)

    redisInstance.setex('company:{}:preds'.format(
        companyID), 1800, preds.to_msgpack())
    redisInstance.setex('company:{}:products'.format(
        companyID), 1800, products.to_msgpack())
    redisInstance.setex('company:{}:ratings'.format(
        companyID), 1800, ratings.to_msgpack())

    return preds, products, ratings


def getDataFromRedis(companyID):
    preds = pd.read_msgpack(redisInstance.get(
        'company:{}:preds'.format(companyID)))
    products = pd.read_msgpack(redisInstance.get(
        'company:{}:products'.format(companyID)))
    ratings = pd.read_msgpack(redisInstance.get(
        'company:{}:ratings'.format(companyID)))

    return preds, products, ratings


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

        r = requests.post(url, headers=headers, data=payload)

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


def fakeCPF():
    return '{}.{}.{}-{}'.format(
        str(random.randint(0, 9))*3,
        str(random.randint(0, 9))*3,
        str(random.randint(0, 9))*3,
        str(random.randint(0, 9))*2
    )


def getPessoas(numPessoas):
    url = 'https://randomuser.me/api?nat=br&results={}&exc=location,dob,id,picture,gender'.format(numPessoas)

    req = requests.get(url)
    usuarios = []
    pessoas = req.json()['results']

    for pessoa in pessoas:
        usuario = {
            'username': pessoa['login']['username'],
            'first_name': str(pessoa['name']['first']).capitalize(),
            'last_name': str(pessoa['name']['last']).capitalize(),
            'email': pessoa['email'],
            'password': pessoa['login']['password'],
            'cpf': fakeCPF(),
            'phone': pessoa['phone'],
            'user_permissions': [],
            'groups': []
        }
        usuarios.append(usuario)

    return usuarios


def cadastrarClientes(users):    
    group_client_ids = list(Group.objects.filter(
        name="client").values_list('id', flat=True))

    for user in users:
        cliente = Client(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=make_password(user['password']),
            phone=user['phone'],
        )
        cliente.save()
        cliente.groups.set(group_client_ids)        


def gerarAvaliacoes(companyID):
    empresa = Company.objects.get(pk=companyID)
    produtos = list(Product.objects.filter(company=empresa))
    clientes = list(Client.objects.all())

    for cliente in clientes:
        print(cliente.id)
        produtos_avaliados = []
        num_avaliacoes = random.randint(0, len(produtos) - 1)
        if num_avaliacoes > 0:
            for j in range(num_avaliacoes):
                produto = random.choice(produtos)
                if produto not in produtos_avaliados:
                    produtos_avaliados.append(produto)
                    avaliacao = Avaliation(
                        company=empresa,
                        client=cliente,
                        note=random.randint(1, 10),
                        product=produto
                    )
                    avaliacao.save()