import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib import constants
from lib.models import (
    Base,
    Genre,
    Movie,
    TVShow,
    Person,
    SearchResult,
    actor_movie,
    actor_tvshow,
    result_tvshow,
    result_movie,
    result_person
)

def get_db(db_uri=None):
    """
    Connects to the default database or the optionally passed *db_uri* and returns a session.
    """
    engine = create_engine(db_uri or constants.database_uri)
    db = sessionmaker()
    db.configure(bind=engine)
    Base.metadata.create_all(engine)
    return db()

def store_model(model, db_uri=None):
    """Caches the passed *model* in the database."""
    try:
        db = get_db(db_uri)
        db.add(model)
        db.commit()
        db.close()
        return True
    except(sqlalchemy.exc.IntegrityError, sqlalchemy.orm.exc.UnmappedInstanceError):
        pass
    return False

def store_cast_member(model, person, db_uri=None):
    """Adds a person to either a tv show or movie as a member of the cast."""
    try:
        db = get_db(db_uri)
        if isinstance(model, Movie):
            db.execute(actor_movie.insert().values([(person.id, model.id)]))
        else:
            db.execute(actor_tvshow.insert().values([(person.id, model.id)]))
        print('<{}> -> <{}>'.format(person.id, model.id))
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        pass
    finally:
        db.close()

def get_cached_model(model_id, db_uri=None):
    """
    Returns a cached model from the database if it matches the *model_id*.
    None is returned when we don't have the model cached yet.
    """
    if isinstance(model_id, bytes):
        model_id = model_id.decode('utf-8')
    db = get_db(db_uri)
    for m in (Movie, TVShow, Person):
        existing_model = db.query(m).get(model_id)
        if existing_model:
            db.close()
            return existing_model

def store_search_result(query, model, db_uri=None):

    db = get_db(db_uri)
    try:
        sr = SearchResult(query)
        db.add(sr)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()

    try:
        if isinstance(model, Movie):
            db.execute(result_movie.insert().values([query, model.id]))
        elif isinstance(model, TVShow):
            db.execute(result_tvshow.insert().values([query, model.id]))
        elif isinstance(model, Person):
            db.execute(result_person.insert().values([query, model.id]))
    except sqlalchemy.exc.IntegrityError as e:
        db.close()
    else:
        db.commit()
        db.close()

def get_search_results(query, db_uri=None):
    db = get_db(db_uri)
    search_result = db.query(SearchResult).get(query)
    if search_result:
        for model_family in (search_result.people, search_result.movies, search_result.tvshows):
            for model in model_family.all():
                if model:
                    yield model
    db.close()

def get_db_stats(db_uri=None):
    """
    Returns a dict containing the count of all records in the database.
    """
    db = get_db(db_uri)
    stats = {'movies': db.query(Movie).count(),
             'tv shows': db.query(TVShow).count(),
             'genres': db.query(Genre).count(),
             'people': db.query(Person).count()}
    db.close()
    return stats
