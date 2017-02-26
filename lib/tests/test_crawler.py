import os
import unittest
import json
import tempfile

from lib import crawl

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
            assert model.id == 'nm0233391'
            break

    def test_models_from_json(self):
        with open(os.path.join(self.here, 'files', 'search_result.json')) as f:
            json_data = json.loads(f.read())
        for model in crawl.models_from_json(json_data, self.db_uri):
            assert model.id == 'tt0133093'
            break

    @classmethod
    def tearDownClass(cls):
        cls.db_session.close()
        cls.db_fd.close()
        os.unlink(cls.db_filepath)


if __name__ == '__main__':
    unittest.main()
