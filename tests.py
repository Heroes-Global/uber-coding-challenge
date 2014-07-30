#!/usr/bin/env python

# # Imports

import os
import unittest

from config import BASE_DIR
from app import app, models
import urllib2
import json

# # Classes


class TestCase(unittest.TestCase):

    # ## Scaffolding

    def setUp(self):
        self.app = app.test_client()
        self.baseUrl = "http://localhost:5000/sfmovies/api/"

    def tearDown(self):
        pass

    # ## Tests

    # ### API Version 1.0 tests

    # /movies

    def test_movies_1_0_director_should_be_charles_chaplin(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
        assert jsonResponse['movies'][0]['director'] == "Charles Chaplin"

    def test_movies_1_0_title_should_be_greed(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
        assert jsonResponse['movies'][3]['title'] == "Greed"

    def test_movies_1_0_writer_should_be_ben_hecht(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
        assert jsonResponse['movies'][6]['writer'] == "Alfred A. Cohn"

    # /movies/<id>

    def test_movies_1_0_movie_should_have_year_1923(self):
        movieID = 3
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1.0/movies/" + str(movieID)))
        assert jsonResponse['movie']['year'] == 1923

    # /movies?title

    def test_movie_1_0_the_jazz_singer_should_have_one_results(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1.0/movies?title=The+Jazz+Singer"))
        assert len(jsonResponse['movies']) == 1

    def test_movie_1_0_greed_should_have_three_results(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1.0/movies?title=Greed"))
        assert len(jsonResponse['movies']) == 3

    # /titles

    def test_movies_1_0_title_should_be_ten_commandments(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1.0/titles"))
        assert jsonResponse['titles'][2] == "Play it Again, Sam"

    # ### Model tests

    def test_model_greed_movie_location_should_have_zasu_pitts(self):
        greed = models.MovieLocation(
            title='Greed',
            year=1924,
            location='Hayes Street at Laguna',
            fun_fact='',
            production_company='Metro-Goldwyn-Mayer (MGM)',
            distributor='Metro-Goldwyn-Mayer (MGM)',
            director='Eric von Stroheim',
            writer='Eric von Stroheim',
            actor_1='Zasu Pitts',
            actor_2='',
            actor_3='Cloris Leachman',
            latitude=37.7764647,
            longitude=-122.4262985)
        assert greed.actor_1 == 'Zasu Pitts'

if __name__ == '__main__':
    unittest.main()
