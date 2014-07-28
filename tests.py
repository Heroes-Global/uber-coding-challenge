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
    None

  def test_movies_version_1_0(self):
    jsonResponse = json.load(urllib2.urlopen(self.baseUrl + "v1.0/movies"))
    assert len(jsonResponse['movies']) == 8
    assert jsonResponse['movies'][0]['director'] == "Charles Chaplin"
    assert jsonResponse['movies'][3]['title'] == "Greed"
    assert jsonResponse['movies'][7]['writer'] == "Ben Hecht"

if __name__ == '__main__':
  unittest.main()
