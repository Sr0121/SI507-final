import os
import pandas as pd
import json
from models import Base, Movie, Staff, Cast, Crew, Genre
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///movie.db", echo=True, future=True)


def init_database(credit_file_path, movie_file_path):
    if os.path.exists("./movie.db"):
        return
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        credits_data = pd.read_csv(credit_file_path)
        movie_data = pd.read_csv(movie_file_path)
        staff_map = {}
        movie_map = {}
        genre_map = {}
        for _, row in credits_data.iterrows():
            movie = Movie(id=row["movie_id"], title=row["title"])
            casts = json.loads(row["cast"])
            for cast in casts:
                if cast["id"] not in staff_map:
                    staff_map[cast["id"]] = Staff(id=cast["id"], name=cast["name"], gender=cast["gender"])
                new_cast = Cast(character=cast["character"])
                staff_map[cast["id"]].casts.append(new_cast)
                movie.casts.append(new_cast)

            crews = json.loads(row["crew"])
            for crew in crews:
                if crew["id"] not in staff_map:
                    staff_map[crew["id"]] = Staff(id=crew["id"], name=crew["name"], gender=crew["gender"])
                new_crew = Crew(department=crew["department"], job=crew["job"])
                staff_map[cast["id"]].crews.append(new_crew)
                movie.crews.append(new_crew)

            movie_map[row["movie_id"]] = movie

        for _, row in movie_data.iterrows():
            genres = json.loads(row["genres"])
            for genre in genres:
                if genre["id"] not in genre_map:
                    genre_map[genre["id"]] = Genre(id=genre["id"], name=genre["name"])
                movie_map[row["id"]].genres.append(genre_map[genre["id"]])

        staff_list = [v for v in staff_map.values()]
        movie_list = [v for v in movie_map.values()]
        session.add_all(staff_list + movie_list)
        session.commit()
