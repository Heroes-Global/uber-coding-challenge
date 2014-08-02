#!/usr/bin/env python

# # Imports

import os
import unittest

from config import BASE_DIR
from app import app
from app import models
from app import errors

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

    # ### API Version 1 tests

    # GET /moviesnotthere

    def test_v1_moviesnotthere_should_have_error_message(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/moviesnotthere")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['message'] == "No resource behind the URI"

    # GET /movies

    def test_v1_movies_id_should_be_37(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][36]['id'] == 37

    def test_v1_movies_title_should_be_greed(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][3]['title'] == "Greed"

    def test_v1_movies_year_should_be_1942(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][17]['year'] == 1942

    def test_v1_movies_location_should_be_bay_bridge(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][15]['location'] == "Ferry Building"

    def test_v1_movies_fun_fact_should_be_exteriors_etc(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][2]['fun_fact'] == "Exteriors of the " + \
            "church were used."

    def test_v1_movies_production_company__should_be_rko(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][27]['production_company'] == "RKO " + \
            "Radio Pictures"

    def test_v1_movies_distributor_should_be_united_artists(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][30]['distributor'] == "United Artists"

    def test_v1_movies_director_should_be_charles_chaplin(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][0]['director'] == "Charles Chaplin"

    def test_v1_movies_writer_should_be_ben_hecht(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][6]['writer'] == "Alfred A. Cohn"

    def test_v1_movies_actor_1_should_be_clark_gable(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][10]['actor_1'] == "Tyrone Power"

    def test_v1_movies_actor_2_should_be_pamela_britton(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][34]['actor_2'] == "Pamela Britton"

    def test_v1_movies_actor_2_should_be_empty(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][39]['actor_2'] == ""

    def test_v1_movies_actor_3_should_be_hector_elizondo(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][45]['actor_3'] == "Hector Elizondo"

    def test_v1_movies_actor_3_should_be_empty(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][44]['actor_3'] == ""

    def test_v1_movies_latitude_should_be_3779276(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][146]['latitude'] == 37.799276

    def test_v1_movies_longitude_should_be_n1224102(self):
        jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1/movies"))
        assert jsonResponse['movies'][84]['longitude'] == -122.4102

    # GET /movies/<id>

    def test_v1_movies_id_3_year_should_be_1923(self):
        movieID = 3
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies/" + str(movieID)))
        assert jsonResponse['movie']['year'] == 1923

    def test_v1_movies_id_42_should_have_title_woman_on_the_run(self):
        movieID = 42
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies/" + str(movieID)))
        assert jsonResponse['movie']['title'] == "Woman on the Run"

    def test_v1_movies_id_97_director_should_be_blake_edwards(self):
        movieID = 97
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies/" + str(movieID)))
        assert jsonResponse['movie']['director'] == "Blake Edwards"

    def test_v1_movies_id_113_writer_should_be_alan_r_trustman(self):
        movieID = 113
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies/" + str(movieID)))
        assert jsonResponse['movie']['writer'] == "Alan R. Trustman"

    def test_v1_movies_id_0_should_have_status_code_404(self):
        movieID = 0
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies/" + str(movieID))
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 404

    def test_v1_movies_id_12345_should_have_error_message(self):
        movieID = 12345
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies/" + str(movieID))
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['message'] == \
                "No movie with id = " + str(movieID)

    # GET /movies?title

    # check lengths
    def test_v1_movies_the_jazz_singer_should_have_one_results(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=The+Jazz+Singer"))
        assert len(jsonResponse['movies']) == 1

    def test_v1_movies_greed_should_have_three_results(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Greed"))
        assert len(jsonResponse['movies']) == 3

    def test_v1_movies_jam_should_have_zero_results(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Jam"))
        assert len(jsonResponse['movies']) == 0

    # check properties
    def test_v1_movies_bullitt_should_have_title_bullitt(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Bullitt"))
        assert jsonResponse['movies'][0]['title'] == "Bullitt"

    def test_v1_movies_take_the_money_should_have_director_woody_allen(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Take+the+Money+and+Run"))
        assert jsonResponse['movies'][1]['director'] == "Woody Allen"

    def test_v1_bullitt_should_have_location_marina_green(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Bullitt"))
        assert jsonResponse['movies'][4]['location'] == "Marina Green " + \
            "(Marina District)"

    # GET /movies?year

    # GET /movies?title&year

    def test_movies_v1_vertigo_1958_should_have_length_16(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Vertigo&year=1958"))
        assert len(jsonResponse['movies']) == 16

    def test_movies_v1_vertigo_1959_should_have_length_0(self):
        jsonResponse = json.load(urllib2.urlopen(
            self.baseUrl + "v1/movies?title=Vertigo&year=1959"))
        assert len(jsonResponse['movies']) == 0

    # GET /movies?sort

    # GET /movies?director&sort

    # GET /movies?fields

    # GET /movies?year&fields&sort

    # ### Model tests

    def test_model_greed_should_have_actor_zasu_pitts(self):
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

    def test_model_vertigo_should_have_year_director_alfred_hitchcock(self):
        vertigo = models.MovieLocation(
            title="Vertigo",
            year=1958,
            location="San Francisco Drydock (20th and Illinois Streets)",
            fun_fact="",
            production_company="Alfred J. Hitchcock Productions",
            distributor="Paramount Pictures",
            director="Alfred Hitchcock",
            writer="Alec Coppel",
            actor_1="James Stewart",
            actor_2="Kim Novak",
            latitude=37.7561141,
            longitude=-122.3871395)
        assert vertigo.director == 'Alfred Hitchcock'


if __name__ == '__main__':
    unittest.main()
