# api.py

# ## Imports

from flask import url_for, jsonify, abort, request
from flask.ext.cors import cross_origin
from app import app

# ## Resources

movie_list = [
  { "id" : 1,
    "release_year" : "1915",
    "title" : "A Jitney Elopement",
    "fun_facts" : "During San Francisco's Gold Rush era, the Park was part of an area designated as the \"Great Sand Waste\". ",
    "writer" : "Charles Chaplin",
    "actor_1" : "Charles Chaplin",
    "locations" : "Golden Gate Park",
    "longitude" : -122.4862138,
    "director" : "Charles Chaplin",
    "latitude" : 37.7694208,
    "production_company" : "The Essanay Film Manufacturing Company",
    "distributor" : "General Film Company" },
  { "id" : 2,
    "release_year" : "1915",
    "title" : "A Jitney Elopement",
    "writer" : "Charles Chaplin",
    "actor_1" : "Charles Chaplin",
    "locations" : "20th and Folsom Streets",
    "longitude" : -122.4147242,
    "director" : "Charles Chaplin",
    "latitude" : 37.758895,
    "production_company" : "The Essanay Film Manufacturing Company",
    "distributor": "General Film Company" },
  { "id" : 3,
    "release_year" : "1923",
    "title" : "The Ten Commandments",
    "fun_facts" : "Exteriors of the church were used.",
    "writer" : "Jesse L. Lasky, Jr.",
    "actor_1" : "Charlton Heston",
    "locations" : "St. Peter & Paul's Church (666 Filbert Street, Washington Square)",
    "longitude" : -122.410084,
    "actor_2" : "Yul Brynner",
    "director" : "Cecil B. DeMille",
    "latitude" : 37.800781,
    "production_company" : "Paramount Pictures",
    "distributor" : "Paramount Pictures" },
  { "id" : 4,
    "release_year" : "1924",
    "title" : "Greed",
    "writer" : "Eric von Stroheim",
    "actor_1" : "Zasu Pitts",
    "locations" : "Hayes Street at Laguna",
    "actor_3" : "Cloris Leachman",
    "director" : "Eric von Stroheim",
    "latitude" : 37.7764647,
    "production_company" : "Metro-Goldwyn-Mayer (MGM)",
    "longitude" : -122.4262985,
    "distributor" : "Metro-Goldwyn-Mayer (MGM)" },
  { "id" : 5,
    "release_year" : "1924",
    "title" : "Greed",
    "fun_facts" : "In 1887, the Cliff House was severely damaged when the schooner Parallel, abandoned and loaded with dynamite, ran aground on the rocks below.",
    "writer" : "Eric von Stroheim",
    "actor_1" : "Zasu Pitts",
    "locations" : "Cliff House (1090 Point Lobos Avenue)",
    "actor_3" : "Cloris Leachman",
    "director" : "Eric von Stroheim",
    "latitude" : 37.7749295,
    "production_company" : "Metro-Goldwyn-Mayer (MGM)",
    "longitude" : -122.4194155,
    "distributor" : "Metro-Goldwyn-Mayer (MGM)" },
  { "id" : 6,
    "release_year" : "1924",
    "title" : "Greed",
    "writer" : "Eric von Stroheim",
    "actor_1" : "Zasu Pitts",
    "locations" : "Bush and Sutter Streets",
    "actor_3" : "Cloris Leachman",
    "director" : "Eric von Stroheim",
    "latitude" : 37.7873702,
    "production_company" : "Metro-Goldwyn-Mayer (MGM)",
    "longitude" : -122.4234239,
    "distributor" : "Metro-Goldwyn-Mayer (MGM)" },
  { "id" : 7,
    "release_year" : "1927",
    "title" : "The Jazz Singer",
    "writer" : "Alfred A. Cohn",
    "actor_1" : "Al Jolson",
    "locations" : "Coffee Dan's (O'Farrell Street at Powell)",
    "actor_3" : "Amy Adams",
    "director" : "Alan Crosland",
    "latitude" : 37.7749295,
    "production_company" : "Warner Bros. Pictures",
    "longitude" : -122.4194155,
    "distributor" : "Warner Bros. Pictures" }
]

# ## Routes

@app.route('/sfmovies/api/v1.0/movies', methods = ['GET'])
@cross_origin(headers=['Content-Type'])
def get_movies():
  """Returns a JSON representation of the locations of movies shot in San
  Francisco."""

  movies = movie_list

  if request.method == 'GET':
    title = request.args.get('title', None)

    if title is not None:
      print movies
      movies = [movie for movie in movies if movie['title'] == title ]
      print movies

  return jsonify({ 'movies' : movies })

@app.route('/sfmovies/api/v1.0/movies/<int:movie_id>', methods = ['GET'])
def get_movie(movie_id):
  """Return a JSON representation of a movie location shot in San Francisco."""

  movies = movie_list

  movie = filter(lambda m: m['id'] == movie_id, movies)
  if len(movie) == 0:
    abort(404)
  return jsonify({ 'movie' : movie[0] })

@app.route('/sfmovies/api/v1.0/titles', methods = ['GET'])
@cross_origin(headers=['Content-Type'])
def titles():
  """Returns a list of the titles movies shot in San Francisco."""

  movies = movie_list

  titles = list(set(map(lambda m: m['title'], movies)))
  return jsonify({ 'titles' : titles })
