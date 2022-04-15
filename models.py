from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table

Base = declarative_base()


# Definition of table "cast" in database
class Cast(Base):
    __tablename__ = "cast"

    id = Column(Integer, primary_key=True)
    character = Column(String)
    people_id = Column(Integer, ForeignKey("people.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))

    people = relationship("People", back_populates="casts")
    movie = relationship("Movie", back_populates="casts")

    def __repr__(self):
        return "<Cast(character='%s')>" % self.character


# Definition of table "crew" in database
class Crew(Base):
    __tablename__ = "crew"

    id = Column(Integer, primary_key=True)
    department = Column(String)
    job = Column(String)
    people_id = Column(Integer, ForeignKey("people.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))

    people = relationship("People", back_populates="crews")
    movie = relationship("Movie", back_populates="crews")

    def __repr__(self):
        return "<Crew(department='%s', job='%s')>" % (self.department, self.job)


# Definition of table "people" in database
class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(Integer)
    casts = relationship("Cast", order_by=Cast.id, back_populates="people")
    crews = relationship("Crew", order_by=Crew.id, back_populates="people")

    def __repr__(self):
        return "<People(name='%s', gender='%s')>" % (self.name, self.gender)


# Association table to implement a many to many relationship of table movie and genre
movie_genre = Table("movie_genre", Base.metadata,
                    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
                    Column("genre_id", ForeignKey("genre.id"), primary_key=True))


# Definition of table "genre" in database
class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

    def __repr__(self):
        return self.name


# Definition of table "movie" in database
class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    casts = relationship("Cast", order_by=Cast.id, back_populates="movie")
    crews = relationship("Crew", order_by=Crew.id, back_populates="movie")
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")

    def __repr__(self):
        return self.title


# Used to store information obtained online
class Media:
    def __init__(self, json_data=None):
        self.title = json_data["Title"]
        self.year = json_data["Year"]
        self.rated = json_data["Rated"]
        self.released = json_data["Released"]
        self.run_time = json_data["Runtime"]
        self.lang = json_data["Language"]
        self.country = json_data["Country"]
        self.awards = json_data["Awards"]
        self.poster = json_data["Poster"]

    def __str__(self):
        return """%s (%s)
        Rate: %s
        Runtime: %s
        Language: %s
        Country: %s
        Awards: %s
        Poster: %s""" % (self.title, self.released, self.rated, self.run_time,
                         self.lang, self.country, self.awards, self.poster)
