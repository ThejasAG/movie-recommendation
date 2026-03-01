from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas
from recommender import get_recommendations

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies")
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(title=movie.title, genre=movie.genre)
    db.add(db_movie)
    db.commit()
    return {"message": "Movie added successfully"}

@app.get("/movies")
def list_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()

@app.post("/ratings")
def add_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_rating = models.Rating(
        user_id=rating.user_id,
        movie_id=rating.movie_id,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    return {"message": "Rating added successfully"}

@app.get("/users/{user_id}/recommendations")
def recommendations(user_id: int, db: Session = Depends(get_db)):
    return get_recommendations(db, user_id)