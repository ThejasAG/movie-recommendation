from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genre: str

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float