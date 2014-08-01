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

    STATUS_OK = 200

    if not request.values and response.status_code == STATUS_OK:
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


@app.route('/sfmovies/api/v1/movies', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_movies():
    """Returns a JSON representation of the locations of movies shot in San
    Francisco.

    """

    query = models.MovieLocation.query
    parameters = {}

    # Get parameters
    if request.method == 'GET':
        arguments = request.args.items()
        for arg in arguments:
            parameters[arg[0]] = arg[1]

    # filter
    for parameter in parameters:
        parameterValue = parameters[parameter]
        if parameter.endswith('<') or parameter.endswith('>'):
            less_or_greater_than = parameter[-1]
            parameter = parameter[:-1]
            modelValue = getattr(models.MovieLocation, parameter, None)
            if less_or_greater_than == '>':
                query = query.filter(modelValue >= parameterValue)
            else:
                query = query.filter(modelValue <= parameterValue)

        else:
            modelValue = getattr(models.MovieLocation, parameter, None)
            if modelValue is not None:
                query = query.filter(modelValue == parameterValue)

    # sort
    if 'sort' in parameters:
        sort_field = parameters['sort']
        order = sort_field[0]
        if order == '-':
            sort_field = sort_field[1:]
            model_field = getattr(models.MovieLocation, sort_field, None)
            if model_field is not None:
                query = query.order_by(model_field.desc())
        elif order == '+':
            sort_field = sort_field[1:]
            model_field = getattr(models.MovieLocation, sort_field, None)
            if model_field is not None:
                query = query.order_by(model_field)
        else:
            model_field = getattr(models.MovieLocation, sort_field, None)
            if model_field is not None:
                query = query.order_by(model_field)
    else:
        query = query.order_by('id')

    # select
    if 'fields' in parameters:
        fields = parameters['fields'].split(",")
        for field in fields:
            model_field = getattr(models.MovieLocation, field, None)
            if model_field is not None:
                query = query.add_column(model_field)
        query = query.add_column(models.MovieLocation.id)

    # paging
    if 'limit' in parameters:
        query = query.limit(parameters['limit'])

    if 'offset' in parameters:
        query = query.offset(parameters['offset'])

    movies = query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)

    return jsonify({'movies': movies})


@app.route('/sfmovies/api/v1/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    """

    movie = models.MovieLocation.query.filter(
        models.MovieLocation.id == movie_id).first()
    if movie is None:
        abort(404)
    movie = jsonify_movie_location(movie)
    return jsonify({'movie': movie})

# ## Utility functions


def jsonify_movie_location(movie_location):
    """Takes a MovieLocation object and returns its JSON representation.

    """
    fields = ['id', 'title', 'year', 'location', 'fun_fact',
              'production_company', 'distributor', 'director', 'writer',
              'actor_1', 'actor_2', 'actor_3', 'latitude', 'longitude',
              'links']

    json_movie = {}

    for field in fields:
        fieldValue = getattr(movie_location, field, None)
        if fieldValue is not None:
            json_movie[field] = fieldValue

    if 'links' in fields:
        json_movie['links'] = [
            {'rel': 'self',
             'href': '/api/v1/movies/' + str(movie_location.id)}
        ]

    return json_movie
