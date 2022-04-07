from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table

Base = declarative_base()


class Cast(Base):
    __tablename__ = 'cast'

    id = Column(Integer, primary_key=True)
    character = Column(String)
    staff_id = Column(Integer, ForeignKey('staff.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))

    staff = relationship("Staff", back_populates="casts")
    movie = relationship("Movie", back_populates="casts")

    def __repr__(self):
        return "<Cast(character='%s')>" % self.character


class Crew(Base):
    __tablename__ = 'crew'

    id = Column(Integer, primary_key=True)
    department = Column(String)
    job = Column(String)
    staff_id = Column(Integer, ForeignKey('staff.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))

    staff = relationship("Staff", back_populates="crews")
    movie = relationship("Movie", back_populates="crews")

    def __repr__(self):
        return "<Cast(department='%s', job='%s')>" % (self.department, self.job)


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(Integer)
    casts = relationship("Cast", order_by=Cast.id, back_populates="staff")
    crews = relationship("Crew", order_by=Crew.id, back_populates="staff")

    def __repr__(self):
        return "<Staff(name='%s', gender='%s')>" % (self.name, self.gender)


movie_genre = Table('movie_genre', Base.metadata,
                    Column('movie_id', ForeignKey('movie.id'), primary_key=True),
                    Column('genre_id', ForeignKey('genre.id'), primary_key=True))


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship('Movie', secondary=movie_genre, back_populates='genres')

    def __repr__(self):
        return "<Genre(name='%s')>" % self.name


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    casts = relationship("Cast", order_by=Cast.id, back_populates="movie")
    crews = relationship("Crew", order_by=Crew.id, back_populates="movie")
    genres = relationship("Genre", secondary=movie_genre, back_populates='movies')


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
        return self.title + " (" + str(self.released) + ")"
