from django.shortcuts import render
import redis
from django.conf import settings
from django.http import HttpResponse
from recsys.utils.functions import gerarAvaliacoes
from api.models import Avaliation, Company, Product
from recsys.recommender.cb_product import loadData, getUserPreferences, recommend

import pandas as pd
# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT, db=settings.REDIS_DB)


def teste(request):

    products = loadData()
  
    userInput = [
        {'name': '4 Queijos', 'note': 4.5},
        {'name': 'Baiana', 'note': 1},
        {'name': 'Escarola', 'note': 5},
        {'name': 'Napolitana', 'note': 3},
        {'name': 'Portuguesa', 'note': 4},
    ]

    inputData = pd.DataFrame(userInput)
    
    print("Produtos avaliados: \n")
    print(inputData)

    ingredientes, perfil = getUserPreferences(inputData, products)

    print("=" * 110)
    print("Recomendacoes: \n")
    recommend(ingredientes, perfil, products)

    # product_df = read_frame(products, fieldnames = ['id', 'name', 'ingredient'])

    # print(avaliation_df.head())

    # print(list(produto.ingredient.values_list('name', flat=True)))

    # print(product_df.head())
    # gerarAvaliacoes()
    return HttpResponse("teste")
