import os
import urlparse

lib_path = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'database', 'im.db'))
database_uri = 'sqlite:///' + database_path
url_base = 'http://m.imdb.com'
cast_url = urlparse.urljoin(url_base, 'title/{model_id}/fullcredits/cast')
fmt_person = '{id} {firstname} {lastname}'
fmt_title = '{id} {title} {year} {rating}'
