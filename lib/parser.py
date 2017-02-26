import re
import datetime

from bs4 import BeautifulSoup

def model_id(source):
    """Extracts the identifier from the passed model *source*."""
    id_re = re.compile('pageId.+?[\"\']((?:tt|nm)\w+)[\"\']')
    return id_re.search(source).group(1)

def model_ids(source):
    """Returns a set of model identifiers found in the passed *source*."""
    model_id_re = re.compile(u'/((?:tt|nm)\d+)')
    return set(model_id_re.findall(source))

def model_type(source):
    """
    Extracts the type of a model from the passed *source*.
    A model type is a string and can be one of the following:

        - tv_show
        - movie
        - actor
    """
    type_re = re.compile('og:type.+?[\"\'].*?(actor|tv_show|movie)[\"\']')
    return type_re.search(source).group(1)

def title(source):
    """Extracts the title from the passed *source*."""
    title_re = re.compile('og:title.+?[\"\'](.+?)\s+?\(.+?[\"\']')
    match = title_re.search(source).group(1)
    if 'TV Series ' in match:
        match = match.replace('TV Series ', '')
    return match

def poster(source):
    """Extracts the absolute URL to the poster from the passed *source*."""
    poster_re = re.compile('og:image.+?[\"\'](http.+?)[\"\']')
    return poster_re.search(source).group(1)

def rating(source):
    """Extracts the rating from the passed *source*."""
    rating_re = re.compile('(\d+\.\d*)<.+?\/\d+')
    return float(rating_re.search(source).group(1))

def duration(source):
    """Extracts the duration (playtime) from the passed *source*."""
    duration_re = re.compile('datetime=.+?\s+([\d\s\w]+?)\n', re.DOTALL)
    return duration_re.search(source).group(1)

def plot(source):
    """Extracts the plot from the passed *source*."""
    plot_re = re.compile('plot-description[\'\"]>\s+(.+?)(?:\.{3}\s?<a href.+?)?<\/p>',
                         re.DOTALL)
    return plot_re.search(source).group(1).strip()

def release_year(source):
    """Extracts the release year from the passed *source*."""
    year_re = re.compile('sub-header[\"\']>\s+\((\d+).+?\)', re.DOTALL)
    return int(year_re.search(source).group(1))

def genres(source, db_uri=None):
    """Extracts a list of genres from the passed *source*."""
    import constants
    from database import get_db
    from models import Genre

    genre_re = re.compile('itemprop=[\'\"]genre[\'\"]>([\w\-]+?)<')
    genre_strings = genre_re.findall(source)
    db_session = get_db(db_uri or constants.database_uri)

    genre_objects = []
    for genre_string in genre_strings:
        genre = db_session.query(Genre).filter_by(name=genre_string).first()
        if not genre:
            genre = Genre(genre_string)
            db_session.add(genre)
            db_session.commit()
            db_session = get_db(db_uri)

    return genre_objects

#
# Credits page related patterns
#

def cast(source):
    """
    Extracts the credits from a movie or tvshow and returns a list of tuples.
    The tuple consists of two elements: name and id.
    """
    soup = BeautifulSoup(source, 'html.parser')
    return map(lambda a: a.get('href').split('/', 3)[2],
               soup.find(id='fullcredits-content').find_all('a'))

#
# Below be h00mans
#

def fullname(source):
    """
    Extracts the first-, middle- and last name of a person. This function returns a tuple of
    three fields containing the individuals first, middle and last name.
    """

    fullname_re = re.compile('og:title.+?[\"\'](.+?)[\"\']\s')
    fullname = fullname_re.search(source).group(1)

    groups = fullname.split(' ', 2)
    firstname = None
    middlename = None
    lastname = None
    if len(groups) == 1:
        firstname = groups[0]
    if len(groups) == 2:
        firstname = groups[0]
        lastname = groups[1]
    elif len(groups) == 3:
        firstname = groups[0]
        middlename = groups[1]
        lastname = groups[2]

    return firstname, middlename, lastname

def birthday(source):
    """Extracts the birthday date of a person. Returns a datetime.date object."""
    birthday_re = re.compile('time datetime=[\'\"](\d{4}\-\d{1,2}\-\d{1,2})[\'\"]')
    birthday_match = birthday_re.search(source)
    if not birthday_match:
        return None
    year, month, day = birthday_match.group(1).split('-', 3)

    # Some people described on IMDB don't have their full birthday displayed. Here we just
    # munge the month and day into some placeholder value to be able to create the
    # datetime.date object.
    if month == '0':
        month = 1
    if day == '0':
        day = 1

    return datetime.date(year=int(year), month=int(month), day=int(day))

def roles(source):
    """Extracts a persons' movies or tv shows he or she played a part in as an actor."""
    roles = re.compile(r'id=[\'\"]actor-(tt\d+)[\"\']')
    return roles.findall(source)
