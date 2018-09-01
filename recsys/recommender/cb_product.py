from api.models import Company, Product, Avaliation
from django_pandas.io import read_frame
import pandas as pd

def loadData():
    """
    Carrega os dados dos produtos e avaliações do banco.
    Trata os dados e retorna os produtos e avaliações.
    """
    company = Company.objects.get(pk=2)
    # avaliations = Avaliation.objects.filter(company=company)
    products = Product.objects.filter(company=company)

    # avaliation_df = read_frame(
    #   avaliations, 
    #   fieldnames=['id', 'note', 'product', 'client', 'company']
    # )

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

    userProfile = userIngredientTable.transpose().dot(inputProducts['note'])  

    ingredientTable = products.set_index(products['id'])

    ingredientTable = ingredientTable.drop('id', 1).drop('name', 1).drop('ingredients', 1)

    return ingredientTable, userProfile


def recommend(ingredientTable, userProfile, products):
    # Multiplica os gêneros pelos pesos para calcular a média ponderada
    recommendationTable_df = ((ingredientTable*userProfile).sum(axis=1))/(userProfile.sum())

    # Ordena em ordem decrescente
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)    
    print(recommendationTable_df.head())
    # Gera a lista de recomendações
    recomendacoes = products.loc[products['id'].isin(recommendationTable_df.head(10).keys())]
    print(recomendacoes)