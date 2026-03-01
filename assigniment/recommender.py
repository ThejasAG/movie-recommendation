import pandas as pd
from sqlalchemy.orm import Session
from models import Rating, Movie
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations(db: Session, user_id: int):

    ratings = db.query(Rating).all()

    if not ratings:
        return {"message": "No ratings available yet"}

    # Convert to DataFrame
    df = pd.DataFrame([
        {"user_id": r.user_id, "movie_id": r.movie_id, "rating": r.rating}
        for r in ratings
    ])

    # Create user-movie matrix
    user_movie_matrix = df.pivot_table(
        index='user_id',
        columns='movie_id',
        values='rating'
    ).fillna(0)

    if user_id not in user_movie_matrix.index:
        return {"message": "User has no ratings yet"}

    # Compute similarity
    similarity = cosine_similarity(user_movie_matrix)
    similarity_df = pd.DataFrame(
        similarity,
        index=user_movie_matrix.index,
        columns=user_movie_matrix.index
    )

    # Get similar users
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:3]

    recommended_movies = []

    for similar_user in similar_users.index:
        user_ratings = user_movie_matrix.loc[similar_user]
        for movie_id, rating in user_ratings.items():
            if rating > 3 and user_movie_matrix.loc[user_id, movie_id] == 0:
                movie = db.query(Movie).filter(Movie.id == movie_id).first()
                if movie:
                    recommended_movies.append(movie.title)

    return {"recommended_movies": list(set(recommended_movies))}