import os
import pandas as pd
import json
from models import Base, Movie, Staff, Cast, Crew, Genre
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_


# Used to handle database
class Sess:
    def __init__(self):
        # Connect to the database
        self.engine = create_engine("sqlite:///movie.db", future=True)
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        # close the connection to the database
        self.session.close()

    def init_database(self, credit_file_path, movie_file_path):
        """Check if there exists the database file and create the database from the csv files if not.

        Parameters
        ----------
        credit_file_path: str
            the file path to tmdb_5000_credits.csv
        movie_file_path: str
            the file path to tmdb_5000_movies.csv
        """
        # if there exists the database, then return directly
        if os.path.exists("./movie.db"):
            return

        print("Building Database...")
        # create table
        Base.metadata.create_all(self.engine)
        # load data from csv files
        credits_data = pd.read_csv(credit_file_path)
        movie_data = pd.read_csv(movie_file_path)
        staff_map = {}
        movie_map = {}
        genre_map = {}
        # build objects from the csv data
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
        # insert objects to the database
        self.session.add_all(staff_list + movie_list)
        self.session.commit()

    def find_movies(self, genre_list=[], character_list=[], staff_list=[]):
        """search the movie from the input information

        Parameters
        ----------
        genre_list: list
            the genre types that the target movies should have
        character_list: list
            the characters that the target movies should have
        staff_list: list
            the staff names that the target movies should have

        Returns
        -------
        list
            a list of Movies that meet the requirements
        """
        res = self.session.query(Movie)
        for genre in genre_list:
            res = res.filter(Movie.genres.any(Genre.name == genre))
        for ch in character_list:
            res = res.filter(Movie.casts.any(Cast.character == ch))
        for staff in staff_list:
            subquery = self.session.query(Staff.id).filter(Staff.name == staff).subquery()
            res = res.filter(or_(Movie.casts.any(Cast.staff_id.in_(subquery)),
                                 Movie.crews.any(Crew.staff_id.in_(subquery))))
        return res.all()

    def find_all_genres(self):
        """return all kinds of genres in the database

        Returns
        -------
        list
            the list contains all kinds of Genres
        """
        return self.session.query(Genre).all()
