import os
import sys
import argparse
import json

from lib import crawl, models, constants, database

def print_model(model, fmt_person, fmt_title):
    """Prints out a model with the passed *fmt_person* and *fmt_title* format strings."""
    if model.id.startswith('tt'):
        print(fmt_title.format(id=model.id,
                               title=model.title,
                               year=model.release_year,
                               plot=model.plot,
                               poster=model.poster,
                               rating=model.rating))
    else:
        print(fmt_person.format(id=model.id,
                                firstname=model.firstname,
                                middlename=model.middlename or 'N/A',
                                lastname=model.lastname or 'N/A'))

def index_routine(args):
    """Indexes as many models as possible either by reading from a source file, passed by the
    -f / --file argument, or by crawling an URL directly which is passed by -u / --url."""
    if args.url:
        for model in crawl.models_from_url(args.url):
            if isinstance(model, models.Person) and args.without_roles is False:
                crawl.extract_acts_by_person(model)
            if isinstance(model, (models.Movie, models.TVShow)) and args.without_cast is False:
                crawl.extract_cast(model)
            print_model(model, args.format_person, args.format_title)
    else:
        with open(args.file) as source_file:
            source = source_file.read()
        for model in crawl.models_from_source(source):
            if isinstance(model, models.Person) and args.without_roles is False:
                crawl.extract_acts_by_person(model)
            if isinstance(model, (models.Movie, models.TVShow)) and args.without_cast is False:
                crawl.extract_cast(model)
            print_model(model, args.format_person, args.format_title)

def search_routine(args):

    encoded_query = crawl.encode_search_query(args.query)
    if not encoded_query:
        print('Search query was empty after encoding it.')
        exit(1)

    # Query our database for a cached search result set before making an actual web request.
    cached_models = database.get_search_results(encoded_query)
    had_models = False
    for model in cached_models:
        if model:
            had_models = True
            print_model(model, args.format_person, args.format_title)
    if had_models:
        return

    query_url = u'https://v2.sg.media-imdb.com/suggests/{}/{}.json'
    json_result_raw = crawl.process_url(query_url.format(encoded_query[0], encoded_query))
    if json_result_raw:
        json_result = json.loads(json_result_raw.split('(', 1)[1][:-1])
        for model in crawl.models_from_json(json_result):
            if model:
                print_model(model, args.format_person, args.format_title)

def main(args):

    if args.command == 'index':
        index_routine(args)
    else:
        search_routine(args)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--format-title', default=constants.fmt_title,
                    help="""
                    A format string used to print out titles.
                    Available placeholders are:

                        {id}
                        {title}
                        {rating}
                        {plot}
                        {year}
                        {poster}
                    """)
    ap.add_argument('-p', '--format-person', default=constants.fmt_person,
                    help="""
                    A format string used to print people.
                    Available placeholders are:

                        {id}
                        {firstname}
                        {middlename}
                        {lastname}
                    """)

    sub_parsers = ap.add_subparsers(dest='command')
    sub_parsers.required = True

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('-q', '--query', required=True)

    index_parser = sub_parsers.add_parser('index')
    index_parser.add_argument('--without-cast', action='store_true', default=False,
                              help='Disable the indexing of tvshow|movie -> actor')
    index_parser.add_argument('--without-roles', action='store_true', default=False,
                              help='Disable the indexing of people -> movie|tvshow')
    model_source = index_parser.add_mutually_exclusive_group(required=True)
    model_source.add_argument('-u', '--url')
    model_source.add_argument('-f', '--file')

    args = ap.parse_args()

    if os.path.isdir(constants.database_dir) is False:
        os.mkdir(constants.database_dir)

    if args.format_title:
        opening_b = args.format_title.count('{')
        closing_b = args.format_title.count('}')
        if opening_b != closing_b:
            sys.stderr.write('--format-title must contain equal '
                             'amounts of opening and closing brackets.\n')
            sys.exit(1)
    if args.format_person:
        opening_b = args.format_person.count('{')
        closing_b = args.format_person.count('}')
        if opening_b != closing_b:
            sys.stderr.write('--format-person must contain equal '
                             'amounts of opening and closing brackets.\n')
            sys.exit(1)

    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        sys.exit(1)
