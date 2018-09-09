from api.models import Company, Product, Avaliation
from django_pandas.io import read_frame
import pandas as pd

def loadData():
    """
    Carrega os dados dos produtos e avaliações do banco.
    Trata os dados e retorna os produtos e avaliações.
    """
    company = Company.objects.get(pk=2)    
    products = Product.objects.filter(company=company)    

    dataframe = []
    # Cria uma lista de produtos personalizada
    for p in products:
        dataframe.append(
          {
            'id': p.id,
            'name': p.name,
            'ingredients': list(p.ingredient.values_list('name', flat=True))
          }
        )

    # Gera um dataframe a partir da lista
    product_df = pd.DataFrame(dataframe)
  
    pwg_df = product_df.copy()

    for index, row in product_df.iterrows():
        for ingredient in row['ingredients']:
            pwg_df.at[index, ingredient] = 1

    pwg_df = pwg_df.fillna(0)

    return pwg_df


def getUserPreferences(userData, products):
    inputId = products[products['name'].isin(userData['name'].tolist())]

    inputProducts = pd.merge(inputId, userData)

    inputProducts = inputProducts.drop('ingredients', 1)

    userProducts = products[products['id'].isin(inputProducts['id'].tolist())]

    userProducts = userProducts.reset_index(drop=True)

    userIngredientTable = userProducts.drop('id', 1).drop('name', 1).drop('ingredients', 1)    

    # Reorganiza a matriz, transformando linhas em colunas e vice-versa
    # Multiplica a matriz pelo número de views de cada produto
    userProfile = userIngredientTable.transpose().dot(inputProducts['views'])

    ingredientTable = products.set_index(products['id'])

    ingredientTable = ingredientTable.drop('id', 1).drop('name', 1).drop('ingredients', 1)

    userProfile = userProfile.sort_values(ascending=False)

    return ingredientTable, userProfile


def recommend(ingredientTable, userProfile, products, userInput):
    
    products_seen = userInput.name.tolist()

    # Multiplica os gêneros pelos pesos para calcular a média ponderada
    recommendationTable_df = ((ingredientTable * userProfile).sum(axis=1)) / (userProfile.sum())

    # Ordena em ordem decrescente
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)    

    # Gera a lista de recomendações
    recomendacoes = products.loc[products['id'].isin(recommendationTable_df.head(10).keys())]
    
    for p in products_seen:
      recomendacoes = recomendacoes[recomendacoes.name != p]

    recomendacoes = recomendacoes[['id', 'ingredients', 'name']]

    print(recomendacoes.head())