import os

import unittest

from lib import models, factory
from lib.database import get_db

class TestModelFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_uri = 'sqlite://'
        cls.db_session = get_db(cls.db_uri)
        cls.here = os.path.dirname(__file__)

    def test_movie_builder(self):
        with open(os.path.join(self.here, 'files', 'the_matrix.html')) as f:
            movie_source = f.read()
        movie = factory.model_builder(movie_source, self.db_uri)
        assert isinstance(movie, models.Movie) == True

    def test_tvshow_builder(self):
        with open(os.path.join(self.here, 'files', 'black_mirror.html')) as f:
            tvshow_source = f.read()
        tvshow = factory.model_builder(tvshow_source, self.db_uri)
        assert isinstance(tvshow, models.TVShow) == True

    def test_person_builder(self):
        with open(os.path.join(self.here, 'files', 'morgan_freeman.html')) as f:
            person_source = f.read()
        person = factory.model_builder(person_source)
        assert isinstance(person, models.Person) == True

    @classmethod
    def tearDownClass(cls):
        cls.db_session.close()
