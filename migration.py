import json

from config.db_conexion import DbConexion
from model.movie import create_movie
from repository.movie_repository import MovieRepository

db_conexion = DbConexion()
movie_repository = MovieRepository(db_conexion)

def read_files(path):
    lines = list()
    with open(path) as file:
        for linea in file:
            lines.append(create_movie(json.loads(linea)))
    return lines



if __name__ == '__main__':
    movies = read_files('resources/NetflixOriginals.json')
    movie_repository.insert_movies(list(map(lambda m: m.insert_query(), movies)))

