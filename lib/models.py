from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Genre(Base):

    __tablename__ = 'tbl_genre'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

class Movie(Base):

    __tablename__ = 'tbl_movie'

    id = Column(String, primary_key=True)
    title = Column(String(256), nullable=False)
    poster = Column(String(256))
    rating = Column(Float)
    plot = Column(String)
    duration = Column(String)
    release_year = Column(Integer)

    genres = relationship('Genre', secondary='tbl_genre_movie')
    actors = relationship('Person', secondary='tbl_actor_movie', lazy='dynamic',
                          backref='movie_roles')

    def __init__(self, id, title, poster, rating, plot, duration, release_year, genres):
        self.id = id
        self.title = title
        self.poster = poster
        self.rating = rating
        self.plot = plot
        self.duration = duration
        self.release_year = release_year
        self.genres = genres

class TVShow(Base):

    __tablename__ = 'tbl_tvshow'

    id = Column(String, primary_key=True)
    title = Column(String(256))
    poster = Column(String(256))
    rating = Column(Float)
    plot = Column(String(2000))
    release_year = Column(Integer)

    genres = relationship('Genre', secondary='tbl_genre_tvshow')
    actors = relationship('Person', secondary='tbl_actor_tvshow',
                          lazy='dynamic', backref='tv_roles')

    def __init__(self, id, title, poster, rating, plot, release_year, genres):
        self.id = id
        self.title = title
        self.poster = poster
        self.rating = rating
        self.plot = plot
        self.release_year = release_year
        self.genres = genres

class Person(Base):

    __tablename__ = 'tbl_person'
    id = Column(String, primary_key=True)
    firstname = Column(String(256), nullable=False)
    middlename = Column(String(256))
    lastname = Column(String(256))
    birthday = Column(Date)

    def __init__(self, id, firstname, lastname=None, birthday=None, middlename=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.middlename = middlename

class SearchResult(Base):

    __tablename__ = 'tbl_search_result'
    query = Column(String, primary_key=True)

    people = relationship('Person', secondary='tbl_result_person', lazy='dynamic')
    tvshows = relationship('TVShow', secondary='tbl_result_tvshow', lazy='dynamic')
    movies = relationship('Movie', secondary='tbl_result_movie', lazy='dynamic')

    def __init__(self, query):
        self.query = query


genre_movie = Table('tbl_genre_movie', Base.metadata,
                    Column('genre_id', String, ForeignKey('tbl_genre.id'), primary_key=True),
                    Column('movie_id', String, ForeignKey('tbl_movie.id'), primary_key=True))
genre_tvshow = Table('tbl_genre_tvshow', Base.metadata,
                     Column('genre_id', String, ForeignKey('tbl_genre.id'), primary_key=True),
                     Column('tvshow_id', String, ForeignKey('tbl_tvshow.id'), primary_key=True))

actor_movie = Table('tbl_actor_movie', Base.metadata,
                    Column('actor_id', String, ForeignKey('tbl_person.id'), primary_key=True),
                    Column('movie_id', String, ForeignKey('tbl_movie.id'), primary_key=True))
actor_tvshow = Table('tbl_actor_tvshow', Base.metadata,
                     Column('actor_id', String, ForeignKey('tbl_person.id'), primary_key=True),
                     Column('tvshow_id', String, ForeignKey('tbl_tvshow.id'), primary_key=True))

result_tvshow = Table('tbl_result_tvshow', Base.metadata,
                  Column('query', String, ForeignKey('tbl_search_result.query'), primary_key=True),
                  Column('tvshow_id', String, ForeignKey('tbl_tvshow.id'), primary_key=True))
result_movie = Table('tbl_result_movie', Base.metadata,
                     Column('query', String, ForeignKey('tbl_search_result.query'), primary_key=True),
                     Column('movie_id', String, ForeignKey('tbl_movie.id'), primary_key=True))
result_person = Table('tbl_result_person', Base.metadata,
                      Column('query', String, ForeignKey('tbl_search_result.query'), primary_key=True),
                      Column('person_id', String, ForeignKey('tbl_person.id'), primary_key=True))
