import os
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

lib_path = os.path.realpath(os.path.dirname(__file__))
database_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'database'))
database_path = os.path.join(database_dir, 'im.db')
database_uri = 'sqlite:///' + database_path
url_base = 'http://m.imdb.com'
cast_url = urlparse.urljoin(url_base, 'title/{model_id}/fullcredits/cast')
fmt_person = '{id} {firstname} {lastname}'
fmt_title = '{id} {title} {year} {rating}'
