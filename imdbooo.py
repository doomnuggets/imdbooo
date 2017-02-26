import sys
import argparse
import re
import json

from lib import crawl, models, constants

def print_model(model, fmt_person, fmt_title):
    if model.id.startswith('tt'):
        print fmt_title.format(id=model.id,
                               title=model.title,
                               year=model.release_year,
                               rating=model.rating)
    else:
        print fmt_person.format(id=model.id,
                                firstname=model.firstname,
                                middlename=model.middlename or 'N/A',
                                lastname=model.lastname or 'N/A')

def index_routine(args):

    if args.url:
        for model in crawl.models_from_url(args.url):
            if isinstance(model, models.Person) and args.without_roles is False:
                crawl.extract_acts_by_person(model)
            if isinstance(model, (models.Movie, models.TVShow)) and args.without_cast is False:
                crawl.extract_cast(model)
            print_model(model, args.format_person, args.format_title)
    else:
        with open(args.file) as f:
            source = f.read()
        for model in crawl.models_from_source(source):
            if isinstance(model, models.Person):
                crawl.extract_acts_by_person(model)
            if isinstance(model, (models.Movie, models.TVShow)):
                crawl.extract_cast(model)
            print_model(model, args.format_person, args.format_title)

def search_routine(args):
    query_url = 'http://v2.sg.media-imdb.com/suggests/{}/{}.json'
    encoded_query = re.sub('\W', '', args.query.lower().replace(' ', '_'))
    if len(encoded_query) < 1:
        print 'Search query was empty after encoding it.'
        return

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
                        {year}
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

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('-q', '--query', required=True)

    index_parser = sub_parsers.add_parser('index')
    index_parser.add_argument('--without-cast', action='store_true', default=False)
    index_parser.add_argument('--without-roles', action='store_true', default=False)
    model_source = index_parser.add_mutually_exclusive_group()
    model_source.add_argument('-u', '--url')
    model_source.add_argument('-f', '--file')

    args = ap.parse_args()

    if args.format_title:
        opening_b = args.format_title.count('{')
        closing_b = args.format_title.count('}')
        if opening_b != closing_b:
            print >> sys.stderr, '--format-title must contain equal amounts of opening- and closing brackets.'
            sys.exit(1)
    if args.format_person:
        opening_b = args.format_person.count('{')
        closing_b = args.format_person.count('}')
        if opening_b != closing_b:
            print >> sys.stderr, '--format-person must contain equal amounts of opening- and closing brackets.'
            sys.exit(1)

    sys.exit(main(args))
