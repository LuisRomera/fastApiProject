from fastapi import APIRouter

router = APIRouter()


@router.get("/get_all")
def get_all():
    from main import get_movie_repository
    movies = list(map(lambda m: m.__dict__, get_movie_repository().find_all()))
    return {"movies": str(movies)}


@router.get("/find_movie/{title}")
def find_movie(title: str):
    from main import get_movie_repository
    movies = get_movie_repository().find_movie(title)
    return {"movies": str(movies)}

