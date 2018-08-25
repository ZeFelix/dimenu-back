import pandas as pd
from math import sqrt
import numpy as np

def loadData():
    """ 
    Carrega o dataset MovieLens e trata os dados, removendo colunas desnecessárias.
    Retorna os dataframes de filmes e avaliações
    """
    # Armazena as informacoes dos filmes em um dataframe do pandas
    movies_df = pd.read_csv('data/movies.csv')
    # Armazena as avaliacoes dos filmes
    ratings_df = pd.read_csv('data/ratings.csv')    

    # Expressao regular para remover o ano da coluna titulo    
    movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)    
    movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)    
    movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')

    # Remover espacos em branco gerados pela remocao do ano
    movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())    

    # Remove a coluna de generos 
    movies_df = movies_df.drop('genres', 1)
    
    # Remove a coluna timestamp das avaliacoes
    ratings_df = ratings_df.drop('timestamp', 1)    

    return movies_df, ratings_df


def userProfile(inputMovies, movies, ratings):
    # Filtra os filmes pelo título
    inputId = movies[movies['title'].isin(inputMovies['title'].tolist())]
    # Adiciona os ids aos filmes assistidos
    inputMovies = pd.merge(inputId, inputMovies)
    # Remove colunas desnecessárias
    inputMovies = inputMovies.drop('year', 1)
    
    # Filtra os usuários que assistiram aos mesmos filmes da entrada
    userSubset = ratings[ratings['movieId'].isin(inputMovies['movieId'].tolist())]
    
    # Cria agrupamentos de usuários de acordo com o id
    userSubsetGroup = userSubset.groupby(['userId'])
    
    # Ordena de forma que usuários mais similares com a entrada tenham maior prioridade
    userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
    
    return inputMovies, userSubsetGroup


# Parei aqui
def pearsonCorrelation(userGroup, inputMovies):
    # Dicionário para armazenar o id do usuário e o coeficiente de correlação de Pearson
    pearsonCorrelationDict = {}

    #For every user group in our subset
    for name, group in userGroup:
        # Ordena os dados pelo id do filme
        group = group.sort_values(by='movieId')
        inputMovies = inputMovies.sort_values(by='movieId')
        
        # Calcula o valor de n para a fórmula
        nRatings = len(group)

        # Captura as notas dos filmes em comum entre os usuários
        temp_df = inputMovies[inputMovies['movieId'].isin(group['movieId'].tolist())]        
        tempRatingList = temp_df['rating'].tolist()

        # Converte o grupo numa lista
        tempGroupList = group['rating'].tolist()

        # Calcula os somatório de x
        Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
        # Calcula os somatório de y
        Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
        # Calcula os somatório de x e y
        Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
        
        # Verifica se os valores não são iguais a 0
        if Sxx != 0 and Syy != 0:
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
        else:
            pearsonCorrelationDict[name] = 0
    
    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['userId'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    print(pearsonDF.head())

    return pearsonDF


def recommend(pearsonDF, ratings, movies):
    # Seleciona os 50 usuários mais similares com a entrada
    topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
    # print(topUsers.head())

    # Captura os filmes assistidos pelos usuários na base de dados
    topUsersRating=topUsers.merge(ratings, left_on='userId', right_on='userId', how='inner')
    # print(topUsersRating.head())

    #Multiplies the similarity by the user's ratings
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
    # print(topUsersRating.head())

    #Applies a sum to the topUsers after grouping it up by userId
    tempTopUsersRating = topUsersRating.groupby('movieId').sum()[['similarityIndex','weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
    # print(tempTopUsersRating.head())

    #Creates an empty dataframe
    recommendation_df = pd.DataFrame()
    #Now we take the weighted average
    recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
    recommendation_df['movieId'] = tempTopUsersRating.index
    print(recommendation_df.head())

    recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
    print(recommendation_df.head(10))

    print(movies.loc[movies['movieId'].isin(recommendation_df.head(10)['movieId'].tolist())])


movies, ratings = loadData()
""" 
userInput = [
    {'title':'Breakfast Club, The', 'rating':5},
    {'title':'Toy Story', 'rating':3.5},
    {'title':'Jumanji', 'rating':2},
    {'title':"Pulp Fiction", 'rating':5},
    {'title':'Akira', 'rating':4.5}
]
 """

userInput = [                    
    {'title': 'Iron Man', 'rating': 4.5},
    {'title': 'Avengers: Age of Ultron', 'rating': 5},
    {'title': 'Ant-Man', 'rating':5},            
    {'title': 'Guardians of the Galaxy', 'rating': 5},
    {'title': 'X-Men Origins: Wolverine', 'rating': 2},
    {'title': 'Thor: The Dark World', 'rating': 4},
    # {'title': 'Dracula', 'rating': 5},
    # {'title': 'Fog', 'rating': 2},
    # {'title': 'Howling', 'rating': 4},
]

inputMovies = pd.DataFrame(userInput)

watchedMovies, userGroup  = userProfile(inputMovies, movies, ratings)

pearson = pearsonCorrelation(userGroup, watchedMovies)

recommend(pearson, ratings, movies)
