class Movie:

    def __init__(self, genre, score, language, premiere, runtime, title):
        self.genre = genre
        self.score = score
        self.language = language
        self.premiere = premiere
        self.runtime = runtime
        self.title = title


    def insert_query(self):
        return ("insert into movie(title,genre,premiere,runtime,score,language) values (?,?,?,?,?,?)",
                self)


def create_movie(json):
    return Movie(json['Genre'], float(json['IMDB Score']), json['Language'], json['Premiere'], int(json['Runtime']), json['Title'])