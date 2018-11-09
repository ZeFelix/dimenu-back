from api.models import Company, Product, Avaliation
from django_pandas.io import read_frame
import pandas as pd

class CBRecommender(object):

    def __init__(self, ml=False, hybrid=False, data=None):
        self.ml = ml
        self.hybrid = hybrid
        if hybrid:
            self.data = data


    def loadData(self, companyID, data = None):
        """
        Carrega os dados dos produtos e avaliações do banco.
        Trata os dados e retorna os produtos e avaliações.
        """
        if self.hybrid:
            dataframe = self.data.copy()
            if self.ml:
                dataframe['features'] = dataframe.features.str.split('|')

            # Para cada filme, marca o genero existente nele com o número 1
            for index, row in dataframe.iterrows():
                for feat in row['features']:
                    dataframe.at[index, feat] = 1

            # Para os generos não existentes nos filmes, marca o número 0
            dataframeN = dataframe.fillna(0)
            return dataframeN

        else:
            if not self.ml:
                company = Company.objects.get(pk=companyID)
                products = Product.objects.filter(company=company)

                dataframe = []
                # Cria uma lista de produtos personalizada
                for p in products:
                    dataframe.append(
                    {
                        'itemId': p.id,
                        'name': p.name,
                        'features': list(p.ingredient.values_list('name', flat=True))
                    }
                    )

                # Gera um dataframe a partir da lista
                product_df = pd.DataFrame(dataframe)

                pwg_df = product_df.copy()

                for index, row in product_df.iterrows():
                    for feat in row['features']:
                        pwg_df.at[index, feat] = 1

                pwg_df = pwg_df.fillna(0)

                return pwg_df

            else:
                dataframe = pd.read_csv('/home/anderson/CodeEnv/Projetos/digimenu/recsys/recommender/data/movies.csv')

                dataframe['features'] = dataframe.features.str.split('|')

                nDataframe = dataframe.copy()

                for index, row in dataframe.iterrows():
                    for feat in row['features']:
                        nDataframe[index,feat] = 1

                # dataframe = dataframe.fillna(0)
                # dataframe = dataframe.drop('timestamp', 1)

                return nDataframe


    def getUserPreferences(self, userData, products):
        print("Itens já avaliados: \n")
        print(userData)

        if self.hybrid:
            userData = userData.drop('features', 1)

        inputId = products[products['name'].isin(userData['name'].tolist())]

        inputProducts = pd.merge(inputId, userData)

        inputProducts = inputProducts.drop('features', 1)
        userProducts = products[products['itemId'].isin(inputProducts['itemId'].tolist())]

        userProducts = userProducts.reset_index(drop=True)

        userIngredientTable = None
        if self.hybrid and not self.ml:
            userIngredientTable = userProducts.drop('itemId', 1).drop('name', 1).drop('features', 1).drop('rating', 1)
        else:
            userIngredientTable = userProducts.drop('itemId', 1).drop('name', 1).drop('features', 1)

        # Reorganiza a matriz, transformando linhas em colunas e vice-versa
        # Multiplica a matriz pelo número de views de cada produto

        userProfile = userIngredientTable.transpose().dot(inputProducts['rating'])

        ingredientTable = products.set_index(products['itemId'])

        if self.hybrid:
            ingredientTable = ingredientTable.drop('itemId', 1).drop('name', 1).drop('features', 1).drop('rating', 1)
        else:
            ingredientTable = ingredientTable.drop('itemId', 1).drop('name', 1).drop('features', 1)

        userProfile = userProfile.sort_values(ascending=False)

        print("\nPerfil de usuário: \n")
        if self.ml:
            userProfile = userProfile.drop(['rating'])
        print(userProfile)

        return ingredientTable, userProfile


    def recommend(self, ingredientTable, userProfile, products, userInput):

        products_seen = userInput.name.tolist()

        # Multiplica os gêneros pelos pesos para calcular a média ponderada
        recommendationTable_df = ((ingredientTable * userProfile).sum(axis=1)) / (userProfile.sum())
        
        # Ordena em ordem decrescente
        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)

        # Gera a lista de recomendações
        recomendacoes = products.loc[products['itemId'].isin(recommendationTable_df.keys()[:10])]
        recomendacoes = recomendacoes[['name', 'features', 'rating']]

        print("\nRecomendações: \n")
        print(recomendacoes)
        return recomendacoes