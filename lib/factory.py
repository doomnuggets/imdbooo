from lib import parser
from lib.models import Movie, TVShow, Person

def movie(source, db_uri=None):
    """
    Builds a movie object from the passed *source* and returns it. The optional parameter
    *db_uri* can be modified to look up genres in a different database if needed. By default
    this parameter uses the *constants.database_uri*.
    """
    return Movie(id=parser.model_id(source),
                 title=parser.title(source),
                 poster=parser.poster(source),
                 rating=parser.rating(source),
                 duration=parser.duration(source),
                 plot=parser.plot(source),
                 release_year=parser.release_year(source),
                 genres=parser.genres(source, db_uri=db_uri))

def tvshow(source, db_uri=None):
    """
    Builds a TVShow object from the passed *source* and returns it. The optional parameter
    *db_uri* can be modified to look up genres in a different database if needed. By default
    this parameter uses *constants.database_uri*.
    """
    return TVShow(id=parser.model_id(source),
                  title=parser.title(source),
                  poster=parser.poster(source),
                  rating=parser.rating(source),
                  plot=parser.plot(source),
                  release_year=parser.release_year(source),
                  genres=parser.genres(source, db_uri=db_uri))

def person(source):
    """Builds a *Person* object from the information in the passed *source*."""
    firstname, middlename, lastname = parser.fullname(source)
    return Person(id=parser.model_id(source),
                  firstname=firstname,
                  lastname=lastname,
                  middlename=middlename,
                  birthday=parser.birthday(source))

def model_builder(source, db_uri=None):
    """
    This function tries to detect what kind of model to build by parsing the passed *source*.
    On Success the parsed model is returned None on failure.

    The optional parameter *db_uri* can be used to specify a different database to use during
    Genre lookups.
    """
    try:
        model_type = parser.model_type(source)
        if model_type == 'tv_show':
            return tvshow(source, db_uri=db_uri)
        elif model_type == 'movie':
            return movie(source, db_uri=db_uri)
        elif model_type == 'actor':
            return person(source)
    except AttributeError:
        # Model couldn't be parsed.
        pass
