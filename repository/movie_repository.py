from model.movie import Movie


class MovieRepository:

    def __init__(self, db_conexion):
        self.db_conexion = db_conexion

    def insert_movie(self, query):
        self.db_conexion.conexion.execute(query)
        self.db_conexion.conexion.commint()
    def insert_movies(self, list_query):
        for query in list_query:
            self.db_conexion.conexion.execute(query[0],
                                              (query[1].title, query[1].genre, query[1].premiere, query[1].runtime, query[1].score, query[1].language))
        self.db_conexion.conexion.commit()

    def find_all(self):
        connexion = self.db_conexion.get_db_connection()
        cursor = connexion.cursor()
        cursor = cursor.execute("select id,title,genre,premiere,runtime,score,language from movie")

        movies = list(map(lambda r: Movie(r[1], r[2], r[3], r[4], r[5], r[6]), cursor))
        connexion.close()
        return movies


    def find_movie(self, title):
        connexion = self.db_conexion.get_db_connection()
        cursor = connexion.cursor()
        cursor = cursor.execute("select id,title,genre,premiere,runtime,score,language from movie where title like '%" + title +"%'")

        movies = list(map(lambda r: Movie(r[1], r[2], r[3], r[4], r[5], r[6]).__dict__, cursor))
        connexion.close()
        return movies