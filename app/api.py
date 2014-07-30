# api.py

# ## Imports

from flask import url_for, jsonify, abort, request
from flask.ext.cors import cross_origin
from app import app
from app import models
from app import db

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

    if title is not None:
        movies = [movie for movie in movies if
                  movie['title'].lower() == title.lower()]

    return jsonify({'movies': movies})


@app.route('/sfmovies/api/v1.0/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    """

    movies = models.MovieLocation.query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)

    movie = filter(lambda m: m['id'] == movie_id, movies)
    if len(movie) == 0:
        abort(404)
    return jsonify({'movie': movie[0]})


@app.route('/sfmovies/api/v1.0/titles', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def titles():
    """Returns a list of the titles movies shot in San Francisco.

    """

    movies = models.MovieLocation.query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)

    titles = list(set(map(lambda m: m['title'], movies)))
    return jsonify({'titles': titles})


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
