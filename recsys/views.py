import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from recsys.utils.functions import gerarAvaliacoes, cadastrarClientes, getPessoas, getDataFromRedis, setDataInRedis
from api.models import Avaliation, Company, Product, Client
from recsys.recommender.cb_product import CBRecommender
from recsys.recommender.iter_svd import CFRecommender

# Create your views here.


def addUsers(request, numPessoas):
    cadastrarClientes(getPessoas(numPessoas))
    return HttpResponse('Clientes cadastrados')


def addRatings(request, companyID):
    gerarAvaliacoes(companyID)
    return HttpResponse('Avaliações geradas')


# Iterative SVD
def iterSVD(request, companyID, userID):
    rated = recs = None
    recsys = CFRecommender(companyID=companyID, teta=0.0001, ml=False)

    if recsys.dataLoaded:
        rated, recs = recsys.recommend(userID, 10)

    else:
        recsys.loadData(companyID)
        recsys.itrSVD(companyID)
        rated, recs = recsys.recommend(userID, 10)

    return HttpResponse("Iter SVD")


# Híbrido
def hybrid_recsys(request, companyID, userID):
    rated = recs = None
    movielens = True
    hybrid = True

    cfRecsys = CFRecommender(companyID=companyID, teta=0.0001, ml=movielens)

    # Se os dados já foram calculados
    if cfRecsys.dataLoaded:
        rated, recs = cfRecsys.recommend(userID, 10)
        
        cbRecsys = CBRecommender(ml=movielens, hybrid=hybrid, data=recs)
        itens = cbRecsys.loadData(companyID, data=recs)    
        featTable, profile = cbRecsys.getUserPreferences(rated, itens)
        response = cbRecsys.recommend(featTable, profile, itens, rated)
        response = response.to_dict('records')
        return JsonResponse(response, safe=False)

    else:
        cfRecsys.loadData(companyID)
        cfRecsys.itrSVD(companyID)
        rated, recs = cfRecsys.recommend(userID, 10)

        cbRecsys = CBRecommender(ml=movielens, hybrid=hybrid, data=recs)
        itens = cbRecsys.loadData(companyID, data=recs)
        featTable, profile = cbRecsys.getUserPreferences(rated, itens)
        response = cbRecsys.recommend(featTable, profile, itens, rated)
        response = response.to_dict('records')
        return JsonResponse(response, safe=False)

    return HttpResponse("Sistema híbrido")

# Content-based
def cb_recsys(request, companyID, userID):
    company = Company.objects.get(pk=companyID)
    user = Client.objects.get(pk=userID)
    ratings = Avaliation.objects.filter(company=company)
    ratings = ratings.filter(client=user)
    adf = []
    for a in ratings:
        adf.append(
            {
                'name': a.product.name,
                'rating': a.note
            }
        )
    rated = pd.DataFrame(adf)

    cbRecsys = CBRecommender(ml=False, hybrid=False)
    itens = cbRecsys.loadData(companyID, data=None)    
    featTable, profile = cbRecsys.getUserPreferences(rated, itens)
    print(featTable)
    cbRecsys.recommend(featTable, profile, itens, rated)

    return HttpResponse("Sistema baseado em conteúdo")


def cb_movies(request):
    run()
    return HttpResponse("CB Movies")
