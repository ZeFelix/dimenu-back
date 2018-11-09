import pandas as pd
import numpy as np
from sklearn.utils.extmath import randomized_svd
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from api.models import Company, Product, Avaliation
from math import sqrt
import matplotlib.pyplot as plt
from scipy.linalg import sqrtm
from recsys.utils.functions import redisInstance, getDataFromRedis

class CFRecommender(object):
    
    def __init__(self, companyID, teta=0.0001, ml=False):
        self.difHist = []
        self.error = [0]
        self.idenMatrix = None
        self.mseHist = []
        self.numIterations = 0
        self.rmseHist = []
        self.ml = ml
        try:
            self.predictions, self.products, self.ratings = getDataFromRedis(companyID)
            self.dataLoaded = True
        except Exception as e:
            self.dataLoaded = False
            self.predictions = self.products = self.ratings = None
        self.teta = teta
        

    def itrSVD(self, companyID):
        t = 0        # Contador de iterações
        flag = False  # Flag para saber quando inicializar ou trocar valores

        x, y = np.where(np.isnan(self.idenMatrix))  # Indices dos valores desconhecidos

        # Matrizes usadas no codigo
        R = self.idenMatrix.copy()
        cA = self.idenMatrix.copy()
        pA = None

        while True:
            # Troca os valores desconhecidos na matriz original pelos previstos
            if flag:
                print("Atualizando predicoes...")
                for i, j in zip(x, y):
                    cA[i, j] = pA[i, j]
                print("Atualizacao concluida.\n")

            # Preenche os valores desconhecidos com a média
            else:
                print("Inicializando dados...")
                # cA = np.nan_to_num(cA, 0)
                # R = np.nan_to_num(R, 0)
                means = np.nanmean(a=cA, axis=1)
                for i in range(cA.shape[0]):
                    cA[i][np.isnan(cA[i])] = means[i]    
                print("Inicializacao concluida.\n")
            
            # Aplica SVD
            print("Computando SVD...")
            U, S, V = randomized_svd(cA, n_components=2)
            S = np.diag(S)
            print("SVD obtido.\n")
            # Calcula raiz de S
            s = sqrtm(S)

            # Computa M e N
            M = np.dot(U, s.transpose())
            N = np.dot(s, V)

            # Monta matriz de predições a partir da multiplicação entre M e N
            print("Gerando predicoes...")
            pA = np.dot(M, N)

            print("Predicoes geradas.\n")

            # tmp = np.copy(pA)

            # for i, j in zip(x, y):
            #     tmp[i, j] = 0
            
            print("Calculando taxa de erro...")
            err = mae(y_pred=pA, y_true=cA)
            mse_e = mse(y_pred=pA, y_true=cA)
            rmse_e = sqrt(mse_e)
            print("Erro calculado.\n")

            print("Numero de iteracoes: {}".format(t))
            print("MAE: {:.5f}; MSE: {:.5f}; RMSE: {:.5f}\n".format(
                err, mse_e, rmse_e))
            dif = err - self.error[-1]

            if t >= 1 and abs(dif) <= self.teta:
                self.error.append(err)
                self.mseHist.append(mse_e)
                self.rmseHist.append(rmse_e)
                self.difHist.append(abs(dif))
                self.numIterations = t
                # Atualiza matriz
                for i, j in zip(x, y):
                    cA[i, j] = pA[i, j]

                self.predictions = pd.DataFrame(cA, columns = self.ratings.pivot_table(index='userId', columns='itemId', values='rating').columns)
                redisInstance.setex('company:{}:preds'.format(companyID), 3600, self.predictions.to_msgpack())
                break
            else:
                t += 1
                flag = True
                self.error.append(err)
                self.mseHist.append(mse_e)
                self.rmseHist.append(rmse_e)
                self.difHist.append(abs(dif))        

    def showGraphic(self, data, y_label=None, x_label=None, label=None):
        plt.grid()
        plt.plot(data, color = 'blue', linestyle = '-', label = label)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.show()


    def loadData(self, companyID):
        if not self.ml:
            # Lê a base de dados de produtos e avaliações
            company = Company.objects.get(pk=companyID)
            avaliations = Avaliation.objects.filter(company=company)
            products = Product.objects.filter(company=company)

            adf = []
            for a in avaliations:
                adf.append(
                    {
                        'userId': a.client.id,
                        'itemId': a.product.id,
                        'rating': a.note
                    }
                )

            pdf = []
            # Cria uma lista de produtos personalizada
            for p in products:                
                pdf.append(
                    {
                        'itemId': p.id,
                        'name': p.name,
                        'features': list(p.ingredient.values_list('name', flat=True))                        
                    }
                )

            # Gera um dataframe a partir da lista
            self.products = pd.DataFrame(pdf)
            self.ratings = pd.DataFrame(adf)
        
        else:
            self.products = pd.read_csv(
                '/home/anderson/CodeEnv/Projetos/digimenu/recsys/recommender/data/movies.csv') #.sample(frac=0.2)
            self.ratings = pd.read_csv(
                '/home/anderson/CodeEnv/Projetos/digimenu/recsys/recommender/data/ratings.csv') #.sample(frac=0.2)

        redisInstance.setex('company:{}:products'.format(companyID), 3600, self.products.to_msgpack())
        redisInstance.setex('company:{}:ratings'.format(companyID), 3600, self.ratings.to_msgpack())

        # Reorganiza a tabela para a forma linhas = usuários e colunas = produtos
        Ratings = self.ratings.pivot_table(
            index='userId', columns='itemId', values='rating')
        
        # Gera uma matriz com os valores da base de dados
        self.idenMatrix = Ratings.values
       
        """ self.idenMatrix = np.array([
            [1, -1, 1, -1, 1, -1],
            [1, 1, np.nan, -1, -1, -1],
            [np.nan, 1, 1, -1, -1, np.nan],
            [-1, -1, -1, 1, 1, 1],
            [-1, np.nan, -1, 1, 1, 1]
        ]) """


    def recommend(self, userID, num_recommendations):
        rowNumber = None
        # Os ids de usuários mudam de acordo com a base
        if self.ml:
            rowNumber = userID - 1 
        else:
            rowNumber = userID - 101

        # Get and sort the user's predictions
        sortedPreds = self.predictions.iloc[rowNumber].sort_values(
            ascending=False)  # User ID starts at 1
                    
        # Get the user's data and merge in the movie information.
        user_data = self.ratings[self.ratings.userId == (userID)]        
        user_full = (user_data.merge(self.products, how='left', left_on='itemId',
                                    right_on='itemId').sort_values(['rating'], ascending=False))

        # Recommend the highest predicted rating products that the user hasn't seen yet.
        predicts = (self.products.merge(
            pd.DataFrame(sortedPreds).reset_index(),
            how='left',
            left_on='itemId',
            right_on='itemId').
            rename(columns={rowNumber: 'rating'}).
            sort_values('rating', ascending=False)
        )

        recommendations = (
            self.products[~self.products['itemId'].isin(user_full['itemId'])].
                        merge(pd.DataFrame(sortedPreds).reset_index(), how='left',
                                left_on='itemId',
                                right_on='itemId').
                        rename(columns={rowNumber: 'rating'}).
                        sort_values('rating', ascending=False).
                        iloc[:num_recommendations]
        )

        # recommendations = recommendations.drop('movieId', 1)
        if self.ml:
            user_full = user_full.drop('timestamp', 1).drop('userId', 1)
        else:
            user_full = user_full.drop('userId', 1)

        print('O usuário {} já avaliou {} produtos.'.format(userID, len(user_full)))
        print(user_full)
        print("=" * 120 + '\n')
        print('Recomendando os {} produtos mais bem avaliados.'.format(num_recommendations) + '\n')
        print(recommendations)
        print("=" * 120)
        
        return user_full, predicts
