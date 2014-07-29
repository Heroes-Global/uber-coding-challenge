#!/usr/bin/env python
import os
import unittest

from config import BASE_DIR
from app import app
import urllib2
import json

class TestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()
    self.baseUrl = "http://localhost:5000/sfmovies/api/"

  def tearDown(self):
    pass

  # API Version 1.0 tests

  def test_movies_1_0_director_should_be_charles_chaplin(self):
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
    assert jsonResponse['movies'][0]['director'] == "Charles Chaplin"

  def test_movies_1_0_title_should_be_greed(self):
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
    assert jsonResponse['movies'][3]['title'] == "Greed"

  def test_movies_1_0_writer_should_be_ben_hecht(self):
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
    assert jsonResponse['movies'][6]['writer'] == "Alfred A. Cohn"

  def test_movies_1_0_movie_should_have_release_year_1923(self):
    movieID = 3
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + \
                                             "v1.0/movies/" + str(movieID)))
    assert jsonResponse['movie']['release_year'] == "1923"

  def test_movies_1_0_title_should_be_ten_commandments(self):
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/titles"))
    assert jsonResponse['titles'][2] == "The Ten Commandments"

if __name__ == '__main__':
  unittest.main()
