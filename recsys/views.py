from django.shortcuts import render
from django.http import HttpResponse
from recsys.utils.functions import gerarAvaliacoes, cadastrarClientes, getPessoas, getDataFromRedis, setDataInRedis
from api.models import Avaliation, Company, Product, Client
from recsys.recommender.cb_product import loadData, getUserPreferences, recommend
from recsys.recommender import knn_recsys
from recsys.recommender import cf_products
from recsys.recommender import svd
from surprise import Reader, SVD, evaluate, Dataset
import pandas as pd
# Create your views here.


def teste(request):
    return HttpResponse("teste")


def addUsers(request):
    cadastrarClientes(getPessoas())
    return HttpResponse('Clientes cadastrados')


def addRatings(request):
    gerarAvaliacoes()
    return HttpResponse('Avaliações geradas')


def cb(request):
    products = loadData()

    userdata = [
        {'name': 'Baiana', 'note': 5},
    ]

    userInput = pd.DataFrame(userdata)

    ingredientTable, userProfile = getUserPreferences(userInput, products)

    print(userProfile)

    recommend(ingredientTable, userProfile, products)

    return HttpResponse('CB Recsys')


def cf(request):

    products, ratings = cf_products.loadData()

    userdata = [
        {'name': 'Baiana', 'note': 5},
    ]

    userInput = pd.DataFrame(userdata)

    productsRated, userGroup = cf_products.getUserProfile(
        userInput, products, ratings)

    pearson = cf_products.pearsonCorrelation(userGroup, productsRated)

    recommend(pearson, ratings, products)

    return HttpResponse('CF Recsys')


def svd_rec(request):
    preds = products = ratings = None
    flag = False

    try:
        preds, products, ratings = getDataFromRedis()
    except Exception as e:
        flag = True
        print('#' * 120, 'Dados não carregados em memória', '#' * 120, sep='\n')

    if flag:
        preds, products, ratings = setDataInRedis()

    try:
        already_rated, predictions = svd.recommend_products(
            preds, 150, products, ratings, 5)

        already_rated = already_rated.drop('rating', 1).drop('userId', 1)

        print('O usuário {} já avaliou {} produtos.'.format(150, len(already_rated)))
        print(already_rated.head())
        print("=" * 120 + '\n')
        print('Recomendando os {} produtos mais bem avaliados.'.format(5) + '\n')
        print(predictions)
        print("=" * 120)

        # reader = Reader()

        # data = Dataset.load_from_df(
        #     ratings[['userId', 'productId', 'rating']], reader)

        # data.split(n_folds=5)

        # svd_algo = SVD()

        # print(evaluate(svd_algo, data, measures=['RMSE']))

        # print(ratings[ratings['userId'] == 202])

        # trainset = data.build_full_trainset()
        # svd_algo.train(trainset)

        # print(svd_algo.predict(202, 20))

    except Exception as e:
        print("Erro ao gerar recomendacoes")

    return HttpResponse('SVD Recsys')
