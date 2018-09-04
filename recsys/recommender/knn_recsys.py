import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import sklearn
from sklearn.decomposition import TruncatedSVD
import warnings
from api.models import Company, Product, Avaliation, Client
from django_pandas.io import read_frame


def loadData():
    company = Company.objects.get(pk=2)
    products = Product.objects.filter(company=company)
    users = Client.objects.all()
    ratings = Avaliation.objects.filter(company=company)

    users_df = read_frame(users, fieldnames=['id', 'username'])

    dataframe = []
    # Cria uma lista de produtos personalizada
    for p in products:
        dataframe.append(
            {
                'product_id': p.id,
                'name': p.name,
                'ingredients': list(p.ingredient.values_list('name', flat=True))
            }
        )

    # Gera um dataframe a partir da lista
    products_df = pd.DataFrame(dataframe)

    avaliations = []
    for r in ratings:
        avaliations.append(
            {
                'id': r.id,
                'user': r.client.id,
                'product_id': r.product.id,
                'note': r.note
            }
        )

    ratings_df = pd.DataFrame(avaliations)

    combine_product_rating = pd.merge(ratings_df, products_df, on='product_id')
    colums = ['ingredients']
    combine_product_rating = combine_product_rating.drop(colums, axis=1)    

    combine_product_rating = combine_product_rating.dropna(
        axis=0, subset=['name'])

    product_ratingCount = (combine_product_rating.
                           groupby(by=['name'])['note'].
                           count().
                           reset_index().
                           rename(columns={'note': 'totalRatingCount'})
                           [['name', 'totalRatingCount']]
                           )

    ratingWithCount = combine_product_rating.merge(
        product_ratingCount, left_on='name', right_on='name', how='left')    

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    print(product_ratingCount['totalRatingCount'].describe())

    
    if not ratingWithCount[ratingWithCount.duplicated(['user', 'name'])].empty:
        initial_rows = ratingWithCount.shape[0]
        print('Formato inicial do dataframe {0}'.format(ratingWithCount.shape))
        ratingWithCount = ratingWithCount.drop_duplicates(['user', 'name'])
        current_rows = ratingWithCount.shape[0]

        print('New dataframe shape {0}'.format(ratingWithCount.shape))
        print('Removed {0} rows'.format(initial_rows - current_rows))

    ratingPivot = ratingWithCount.pivot(
        index='user', columns='name', values='note').fillna(0)  

    ratingWithCount = csr_matrix(ratingPivot.values)    

    X = ratingPivot.values.T
    print(X.shape)

    SVD = TruncatedSVD(n_components=12, random_state=17)
    matrix = SVD.fit_transform(X)
    print(matrix.shape)
    
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    corr = np.corrcoef(matrix)
    print(corr.shape)

    ratingsProducts = ratingPivot.columns
    productList = list(ratingsProducts)

    pizza = productList.index('4 Queijos')
    print(pizza)

    corr_pizza = corr[pizza]
    print(list(ratingsProducts[(corr_pizza < 1.0) & (corr_pizza > 0.9)]))