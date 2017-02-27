import os
import random
import unittest
import json
import tempfile

from lib import crawl, models

class TestCrawler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.db_filepath = tempfile.mkstemp()
        cls.db_uri = 'sqlite:///' + cls.db_filepath
        cls.here = os.path.dirname(__file__)

    def test_models_from_source(self):
        with open(os.path.join(self.here, 'files', 'the_matrix.html')) as f:
            movie_source = f.read()
        for model in crawl.models_from_source(movie_source, self.db_uri):
            assert isinstance(model, (models.Movie, models.TVShow, models.Person)) is True
            break

    def test_models_from_json(self):
        with open(os.path.join(self.here, 'files', 'search_result.json')) as f:
            json_data = json.loads(f.read())
        for model in crawl.models_from_json(json_data, self.db_uri):
            assert isinstance(model, models.Movie)
            break

    def test_models_from_url(self):
        for model in crawl.models_from_url('http://m.imdb.com/title/tt{0:7d}'
                                           .format(random.randint(1, 9999999))):
            assert isinstance(model, (models.Movie, models.TVShow, models.Person)) is True
            break

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.db_filepath)


if __name__ == '__main__':
    unittest.main()
