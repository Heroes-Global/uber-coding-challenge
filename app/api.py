# api.py

# ## Imports

from flask import url_for, jsonify, abort, request
from flask.ext.cors import cross_origin
from app import app
from app import models
from app import db
from werkzeug.contrib.cache import SimpleCache  # production: MemcachedCache

# ## Caching


cache = SimpleCache()  # production: cache = MemcachedCache([''])

CLIENT_CACHE_TIMEOUT = 300
SERVER_CACHE_TIMEOUT = 300


@app.before_request
def return_cached():
    """Checks if request is already cached.

    """

    if not request.values:
        response = cache.get(request.path)
        if response:
            return response


@app.after_request
def cache_response(response):
    """Caches a response.

    Arguments:
    - `response`:
    """

    if not request.values:
        cache.set(request.path, response, SERVER_CACHE_TIMEOUT)
    return response


@app.after_request
def add_header(response):
    """

    Arguments:
    - `response`:
    """
    response.cache_control.max_age = CLIENT_CACHE_TIMEOUT
    return response

# ## Resources


@app.route('/sfmovies/api/v1.0/movies', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_movies():
    """Returns a JSON representation of the locations of movies shot in San
    Francisco.

    """

    movies = models.MovieLocation.query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)

    if request.method == 'GET':
        title = request.args.get('title', None)
        year = request.args.get('year', None)

    if title is not None:
        movies = [movie for movie in movies if
                  movie['title'].lower() == title.lower()]

    if year is not None:
        movies = [movie for movie in movies if
                  movie['year'] == int(year)]

    return jsonify({'movies': movies})


@app.route('/sfmovies/api/v1.0/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    """

    movie = models.MovieLocation.query.filter(
        models.MovieLocation.id == movie_id).first()
    if movie is None:
        abort(404)
    movie = jsonify_movie_location(movie)
    return jsonify({'movie': movie})


@app.route('/sfmovies/api/v1.0/titles', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def titles():
    """Returns a list of the titles movies shot in San Francisco.

    """

    titles = models.MovieLocation.query.with_entities(
        models.MovieLocation.title).distinct().all()
    titles = map(lambda title: title[0], titles)
    return jsonify({'titles': titles})


# ## Utility functions


def jsonify_movie_location(movie_location):
    """Takes a MovieLocation object and returns its JSON representation.

    """

    return {
        'id': movie_location.id,
        'title': movie_location.title,
        'year': movie_location.year,
        'location': movie_location.location,
        'fun_fact': movie_location.fun_fact,
        'production_company': movie_location.production_company,
        'distributor': movie_location.distributor,
        'director': movie_location.director,
        'writer': movie_location.writer,
        'actor_1': movie_location.actor_1,
        'actor_2': movie_location.actor_2,
        'actor_1': movie_location.actor_1,
        'latitude': movie_location.latitude,
        'longitude': movie_location.longitude
    }
