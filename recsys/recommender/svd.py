import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from api.models import Company, Product, Avaliation

def loadData(companyID):
    # Lê a base de dados de produtos e avaliações
    company = Company.objects.get(pk=companyID)
    avaliations = Avaliation.objects.filter(company=company)
    products = Product.objects.filter(company=company)

    adf = []
    for a in avaliations:
        adf.append(
            {                
                'userId': a.client.id,
                'productId': a.product.id,
                'rating': a.note
            }
        )

    pdf = []
    # Cria uma lista de produtos personalizada
    for p in products:
        img = ''
        if p.image:
          img = p.image.url
        pdf.append(
            {
                'productId': p.id,
                'name': p.name,
                'ingredients': list(p.ingredient.values_list('name', flat=True)),
                'image': img
            }
        )

    # Gera um dataframe a partir da lista
    product_df = pd.DataFrame(pdf)    
    ratings_df = pd.DataFrame(adf)    

    # Reorganiza a tabela para a forma linhas = usuários e colunas = produtos
    Ratings = ratings_df.pivot_table(index = 'userId', columns = 'productId', values = 'rating').fillna(0)

    # Normaliza os dados  
    R = Ratings.values
    userRatingsMean = np.mean(R, axis = 1)
    ratingsDemeaned = R - userRatingsMean.reshape(-1, 1)

    # Obtem o número de usuários e produtos únicos
    n_users = ratings_df['userId'].unique().shape[0]
    n_products = ratings_df['productId'].unique().shape[0]

    # Calcula a esparsidade dos dados
    sparsity = round(1.0 - len(ratings_df) / float(n_users * n_products), 3)
    print('Sparsity level: {}%'.format(sparsity * 100))
    
    # Aplica o algoritmo SVD aos dados para decompor a matriz
    # U = Matriz unitária esquerda
    # E = Matriz diagonal (pesos)
    # Vt = Matriz unitária direita    
    U, E, Vt = svds(ratingsDemeaned, k = 21)
    E = np.diag(E)

    # Calcula SVD
    userPredictedRatings = np.dot(np.dot(U, E), Vt) + userRatingsMean.reshape(-1, 1)

    preds = pd.DataFrame(userPredictedRatings, columns = Ratings.columns)        

    return preds, product_df, ratings_df

def recommend_products(predictions, userID, products, original_ratings, num_recommendations):
    
    # Get and sort the user's predictions
    user_row_number = userID - 101 # User ID starts at 101, not 0
    sorted_user_predictions = predictions.iloc[user_row_number].sort_values(ascending=False) # User ID starts at 1
  
    # Get the user's data and merge in the movie information.
    user_data = original_ratings[original_ratings.userId == (userID)]     
    user_full = (user_data.merge(products, how = 'left', left_on = 'productId', right_on = 'productId').
                     sort_values(['rating'], ascending=False)
                 )    
    
    # Recommend the highest predicted rating products that the user hasn't seen yet.
    recommendations = (products[~products['productId'].isin(user_full['productId'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'productId',
               right_on = 'productId').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    # recommendations = recommendations.drop('productId', 1)
    user_full = user_full.drop('productId', 1)
    
    return user_full, recommendations