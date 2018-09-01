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

    # Transforma os generos em uma lista
    movies_df['genres'] = movies_df.genres.str.split('|')    

    # Gera uma cópia do dataset de filmes
    moviesWithGenres_df = movies_df.copy()

    # Para cada filme, marca o genero existente nele com o número 1
    for index, row in movies_df.iterrows():
        for genre in row['genres']:
            moviesWithGenres_df.at[index, genre] = 1

    # Para os generos não existentes nos filmes, marca o número 0
    moviesWithGenres_df = moviesWithGenres_df.fillna(0)
    
    # Remove a coluna timestamp
    ratings_df = ratings_df.drop('timestamp', 1)    

    return moviesWithGenres_df, ratings_df


def getUserPreferences(userData, movies, ratings):
    """ 
    Gera uma matriz de preferencias do usuário baseado nos filmes assistidos.
    Retorna uma tabela de gêneros e o perfil do usuário.
    """
    # Captura os ids dos filmes da entrada
    inputId = movies[movies['title'].isin(userData['title'].tolist())]
    # Adiciona os id a cada filme assistido na lista
    inputMovies = pd.merge(inputId, userData)
    # Remove a coluna generos
    inputMovies = inputMovies.drop('genres', 1).drop('year', 1)    

    # Captura os dados dos filmes assistidos na base de dados
    userMovies = movies[movies['movieId'].isin(inputMovies['movieId'].tolist())]    

    # Reseta o indice da busca
    userMovies = userMovies.reset_index(drop=True)
    # Remove colunas desnecessárias dos dados
    userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)    

    # Calcula o produto escalar para gerar os pesos das entradas
    userProfile = userGenreTable.transpose().dot(inputMovies['rating'])    

    # Captura os generos dos filmes na base de dados
    genreTable = movies.set_index(movies['movieId'])
    # Remove colunas desnecessárias
    genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)    

    return genreTable, userProfile


def recommend(genreTable, userProfile, movies):
    # Multiplica os gêneros pelos pesos para calcular a média ponderada
    recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())

    # Ordena em ordem decrescente
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)    

    # Gera a lista de recomendações
    recomendacoes = movies.loc[movies['movieId'].isin(recommendationTable_df.head(10).keys())]
    print(recomendacoes)

    arquivo = open('recomends.txt', 'r+')
    texto = arquivo.readlines()
    texto.append(str(recomendacoes))
    arquivo.writelines(texto)
    arquivo.close()


movies, ratings = loadData()

# Lista de filmes de avaliações dos filmes assistidos
userInput = [                    
    {'title': 'Iron Man', 'rating': 4.5},
    {'title': 'Avengers: Age of Ultron', 'rating': 5},
    {'title': 'Ant-Man', 'rating':5},            
    {'title': 'Guardians of the Galaxy', 'rating': 5},
    # {'title': 'X-Men Origins: Wolverine', 'rating': 2},
    # {'title': 'Thor: The Dark World', 'rating': 4},
    {'title': 'Dracula', 'rating': 5},
    # {'title': 'Fog', 'rating': 2},
    # {'title': 'Howling', 'rating': 4},
]

inputMovies = pd.DataFrame(userInput)
print("=" * 110)
print("Filmes assistidos: \n")
print(inputMovies)

generos, perfil = getUserPreferences(inputMovies, movies, ratings)

print("=" * 110)
print("Recomendacoes: \n")
recommend(generos, perfil, movies)