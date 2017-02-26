try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from io import BytesIO

import pycurl

from lib import constants, factory, parser
from lib.database import (
    store_model,
    get_cached_model,
    get_search_results,
    store_cast_member,
    store_search_result
)

def process_url(url):
    """
    Takes care of submitting a GET request to the passed *url*. The *callback* parameter will
    be used to populate the received data.
    """
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return buffer.getvalue().decode('utf-8')

def extract_cast(model, db_uri=None):
    """
    Extracts the cast from the passed *model*.
    Valid types are *model.Movie* or *model.TVShow*.
    """
    cast_url = constants.cast_url.format(model_id=model.id)
    cast_source = process_url(cast_url)
    people = parser.cast(cast_source)

    for person_id in people:
        person = get_cached_model(person_id, db_uri)
        if person is None:
            # Add the missing person to the database.
            source = process_url(urlparse.urljoin(constants.url_base, 'name/' + person_id))
            new_person = factory.person(source)
            if new_person:
                if store_model(new_person):
                    person = get_cached_model(person_id.decode('utf-8'))
        if person is not None:
            store_cast_member(model, person)

def extract_acts_by_person(person, db_uri=None):
    """Extracts movies or tv shows the passed *person* played in."""
    person_source = process_url('http://www.imdb.com/name/' + person.id)
    for title_id in parser.roles(person_source):
        title = get_cached_model(title_id)
        if title is None:
            # We don't have the movie or tv show cached; index it first.
            source = process_url(urlparse.urljoin(constants.url_base, 'title/' + title_id))
            new_title = factory.model_builder(source)
            if new_title:
                if store_model(new_title):
                    title = get_cached_model(title_id.decode('utf-8'))
        if title is not None:
            store_cast_member(title, person)

def model_url(model_id):
    """
    Helper function to generate the url for extracting a model.
    There are more model aliases out there, but we only support movies and tv shows (tt) and
    names (nm).
    """
    if model_id.startswith('tt'):
        return urlparse.urljoin(constants.url_base, '/'.join(('title', model_id)))
    elif model_id.startswith('nm'):
        return urlparse.urljoin(constants.url_base, '/'.join(('name', model_id)))

def models_from_source(source, db_uri=None):
    for model_id in parser.model_ids(source):
        # Search the database for a cached model matching the current model id.
        cached_model = get_cached_model(model_id, db_uri)
        if cached_model:
            yield cached_model
            continue

        # When we reach this point in the loop the model is not cached in our database.
        # Build the model, cache and yield it.
        _model_url = model_url(model_id)
        if _model_url is None:
            continue

        model_source = process_url(_model_url)
        model = factory.model_builder(model_source, db_uri)
        if model:
            if store_model(model, db_uri):
                yield get_cached_model(model_id.decode('utf-8'), db_uri)

def models_from_json(json_data, db_uri=None):
    """Parses the passed search result *json_data* and extracts the models contained in it."""

    # Before doing any web requests we query our cache database for existing results.
    if get_search_results(json_data.get('q')):
        has_elements = False
        for model in get_search_results(json_data.get('q')):
            if model:
                has_elements = True
                yield model
        if has_elements:
            return

    for result in json_data.get('d'):
        if not result.get('id'):
            continue

        cached_model = get_cached_model(result['id'], db_uri)
        if cached_model:
            store_search_result(json_data.get('q'), cached_model, db_uri)
            yield cached_model
            continue

        _model_url = model_url(result['id'])
        if _model_url is None:
            continue

        model_source = process_url(_model_url)
        model = factory.model_builder(model_source, db_uri)
        if model:
            store_search_result(json_data.get('q'), model, db_uri)
            if store_model(model, db_uri):
                yield get_cached_model(result['id'].decode('utf-8'), db_uri)

def models_from_url(url, db_uri=None):
    """
    Attempts to parse all models from the passed *url*.
    Returns an iterator with models found either in the source or in our database.
    """
    try:
        source = process_url(url)
    except AttributeError:
        print("Failed to find any models in:", url)
        return

    for m in models_from_source(source, db_uri):
        yield m
