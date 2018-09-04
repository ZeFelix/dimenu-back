from api.models import Company, Product, Avaliation
from django_pandas.io import read_frame
import pandas as pd


def loadData():
    """
    Carrega os dados dos produtos e avaliações do banco.
    Trata os dados e retorna os produtos e avaliações.
    """
    company = Company.objects.get(pk=2)
    avaliations = Avaliation.objects.filter(company=company)
    products = Product.objects.filter(company=company)

    adf = []
    for a in avaliations:
        adf.append(
            {
                'id': a.id,
                'user': a.client,
                'product': a.product,
                'note': a.note
            }
        )

    pdf = []
    # Cria uma lista de produtos personalizada
    for p in products:
        pdf.append(
            {
                'id': p.id,
                'name': p.name,
                'ingredients': list(p.ingredient.values_list('name', flat=True))
            }
        )

    # Gera um dataframe a partir da lista
    product_df = pd.DataFrame(pdf)
    ratings_df = pd.DataFrame(adf)

    return product_df, ratings_df


def getUserProfile(userdata, products, ratings):
    inputID = products[products['name'].isin(userdata['name'].tolist())]

    userdata = pd.merge(inputID, userdata)

    userSubset = ratings[ratings['id'].isin(userdata['id'].tolist())]

    userGroups = userSubset.groupby(['user'])

    userGroups = sorted(userGroups, key=lambda x: len(x[1]), reverse=True)

    return userdata, userGroups


def pearsonCorrelation(userGroup, userdata):
    # Dicionário para armazenar o id do usuário e o coeficiente de correlação de Pearson
    pearsonCorrelationDict = {}

    # For every user group in our subset
    for name, group in userGroup:
        # Ordena os dados pelo id do produto
        group = group.sort_values(by='product')
        userdata = userdata.sort_values(by='product')

        # Calcula o valor de n para a fórmula
        nRatings = len(group)

        # Captura as notas dos produtos em comum entre os usuários
        temp_df = userdata[userdata['product'].isin(
            group['product'].tolist())]
        tempRatingList = temp_df['note'].tolist()

        # Converte o grupo numa lista
        tempGroupList = group['note'].tolist()

        # Calcula os somatório de x
        Sxx = sum([i**2 for i in tempRatingList]) - \
            pow(sum(tempRatingList), 2)/float(nRatings)
        # Calcula os somatório de y
        Syy = sum([i**2 for i in tempGroupList]) - \
            pow(sum(tempGroupList), 2)/float(nRatings)
        # Calcula os somatório de x e y
        Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
            sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

        # Verifica se os valores não são iguais a 0
        if Sxx != 0 and Syy != 0:
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
        else:
            pearsonCorrelationDict[name] = 0

    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['user'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    print(pearsonDF.head())

    return pearsonDF

def recommend(pearsonDF, ratings, products):
    # Seleciona os 50 usuários mais similares com a entrada
    topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
    # print(topUsers.head())

    # Captura os filmes assistidos pelos usuários na base de dados
    topUsersRating=topUsers.merge(ratings, left_on='user', right_on='user', how='inner')
    # print(topUsersRating.head())

    #Multiplies the similarity by the user's ratings
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['note']
    # print(topUsersRating.head())

    #Applies a sum to the topUsers after grouping it up by userId
    tempTopUsersRating = topUsersRating.groupby('product').sum()[['similarityIndex','weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
    # print(tempTopUsersRating.head())

    #Creates an empty dataframe
    recommendation_df = pd.DataFrame()
    #Now we take the weighted average
    recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
    recommendation_df['product'] = tempTopUsersRating.index
    print(recommendation_df.head())

    recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
    print(recommendation_df.head(10))

    print(movies.loc[movies['product'].isin(recommendation_df.head(10)['product'].tolist())])
