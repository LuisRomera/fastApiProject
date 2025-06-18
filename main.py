from fastapi import FastAPI

from config.db_conexion import DbConexion
from repository.movie_repository import MovieRepository
from router import MovieRouter

db_conexion = DbConexion()
movie_repository = MovieRepository(db_conexion)


def get_movie_repository():
    return movie_repository


# pip install fastapi uvicorn

app = FastAPI()

app.include_router(MovieRouter.router, prefix="/movie", tags=["movie"])

# uvicorn main:app --reload

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
