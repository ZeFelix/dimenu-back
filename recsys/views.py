from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from recsys.utils.functions import gerarAvaliacoes, cadastrarClientes, getPessoas, getDataFromRedis, setDataInRedis
from api.models import Avaliation, Company, Product, Client
from recsys.recommender.cb_product import loadData, getUserPreferences, recommend
from recsys.recommender import knn_recsys
from recsys.recommender import cf_products
from recsys.recommender import svd
from surprise.model_selection import cross_validate
from surprise import Reader, SVD, evaluate, Dataset
import pandas as pd
from recsys.recommender.iter_svd import Recommender
from recsys.recommender.cb_recsys import run
# Create your views here.


def addUsers(request, numPessoas):
    cadastrarClientes(getPessoas(numPessoas))
    return HttpResponse('Clientes cadastrados')


def addRatings(request, companyID):
    gerarAvaliacoes(companyID)
    return HttpResponse('Avaliações geradas')


def cb(request):
    products = loadData()

    userdata = [
        {'name': 'Baiana', 'views': 3},
        {'name': 'Portuguesa', 'views': 1},
        {'name': '4 Queijos', 'views': 4},
    ]

    userInput = pd.DataFrame(userdata)

    print("\nVocê viu esses items: \n")
    print(userInput.head())

    print("=" * 120, '\n')
    ingredientTable, userProfile = getUserPreferences(userInput, products)

    print("Baseado no se histórico, recomendamos os seguintes items: \n ")
    recommend(ingredientTable, userProfile, products, userInput)
    print("=" * 120, '\n')

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


def svd_rec(request, companyID, userID):
    preds = products = ratings = None
    flag = False
    response = []

    try:
        preds, products, ratings = getDataFromRedis(companyID)
    except Exception as e:
        flag = True
        print('#' * 120, 'Dados não carregados em memória', '#' * 120, sep='\n')

    if flag:
        preds, products, ratings = setDataInRedis(companyID)

    try:
        already_rated, predictions = svd.recommend_products(
            preds, userID, products, ratings, 10)

        already_rated = already_rated.drop('rating', 1).drop('userId', 1)

        print('O usuário {} já avaliou {} produtos.'.format(
            userID, len(already_rated)))
        print(already_rated.head())
        print("=" * 120 + '\n')
        print('Recomendando os {} produtos mais bem avaliados.'.format(5) + '\n')

        tmp = predictions.to_dict('records')
        response = tmp

        print(predictions)
        print("=" * 120)

        # reader = Reader()

        # data = Dataset.load_from_df(
        #     ratings[['userId', 'movieId', 'rating']], reader)

        # algo = SVD()

        # cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # # print(ratings[ratings['userId'] == userID])

        # trainset = data.build_full_trainset()
        # algo.fit(trainset)

        # algo.predict(userID, 12)

    except Exception as e:
        raise(e)
        return HttpResponse('Erro ao gerar recomendacoes')
        print("Erro ao gerar recomendacoes")

    return JsonResponse(response, safe=False)


def iterSVD(request, companyID, userID):

    recsys = Recommender(companyID=companyID, teta=0.0001)

    if recsys.dataLoaded:
        recsys.recommend(userID, 10)
    else:
        recsys.loadData(companyID)
        recsys.itrSVD(companyID)
        recsys.recommend(userID, 10)

    return HttpResponse("Iter SVD")


def cb_movies(request):
    run()
    return HttpResponse("CB Movies")
