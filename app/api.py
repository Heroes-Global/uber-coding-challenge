# api.py

# ## Imports

from flask import url_for, abort, jsonify, request
from flask.ext.cors import cross_origin
from app import app
from app import models
from app import db
from app import errors
from errors import InvalidUsage
from models import MovieLocation
import urllib2

from werkzeug.contrib.cache import SimpleCache  # production: MemcachedCache

# ## Error handling


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handles an error caused by invalid usage of the API.

    Arguments:
    - `error`:
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def handle_invalid_resource_path(error):
    """

    Arguments:
    - `error`:
    """

    response = jsonify({'error': {'status_code': 404,
                                  'message': 'No resource behind the URI'}})
    response.status_code = 404
    return response

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

    PROPERTIES = ['id', 'title', 'writer', 'actor_1', 'actor_2', 'actor_3',
                  'director', 'distributor', 'production_company', 'location',
                  'year', 'fun_fact', 'latitude', 'longitude']

    KEYWORDS = ['sort', 'fields', 'limit', 'offset']

    query = MovieLocation.query
    parameters = {}

    # Get parameters
    if request.method == 'GET':
        arguments = request.args.items()
        for arg in arguments:
            parameters[arg[0]] = arg[1]

    # filter
    for parameter in parameters:

        if parameter in KEYWORDS:
            continue

        parameterValue = parameters[parameter]
        if parameter.endswith('<') or parameter.endswith('>'):

            less_or_greater_than = parameter[-1]
            parameter = parameter[:-1]
            check_parameter_name(parameter, parameterValue, PROPERTIES)
            modelValue = getattr(MovieLocation, parameter, None)
            if modelValue is not None:
                if less_or_greater_than == '>':
                    query = query.filter(modelValue >= parameterValue)
                else:
                    query = query.filter(modelValue <= parameterValue)

        else:

            check_parameter_name(parameter, parameterValue, PROPERTIES)
            modelValue = getattr(MovieLocation, parameter, None)
            if modelValue is not None:
                query = query.filter(modelValue == parameterValue)

    # sort
    if 'sort' in parameters:
        sort_field = parameters['sort']

        if sort_field.startswith('-'):
            sort_field = sort_field[1:]
            check_field(sort_field, PROPERTIES)
            model_field = getattr(MovieLocation, sort_field, None)
            if model_field is not None:
                query = query.order_by(model_field.desc())

        else:
            check_field(sort_field, PROPERTIES)
            model_field = getattr(MovieLocation, sort_field, None)
            if model_field is not None:
                query = query.order_by(model_field)
    else:
        query = query.order_by('id')

    # fields
    if 'fields' in parameters:
        fields = parameters['fields'].split(",")
        for field in fields:
            check_field(field, PROPERTIES)
            model_field = getattr(MovieLocation, field, None)
            if model_field is not None:
                query = query.add_column(model_field)
        query = query.add_column(MovieLocation.id)

    # paging
    if 'limit' in parameters:
        limit = parameters['limit']
        check_paging_value('limit', limit)
        query = query.limit(limit)

    if 'offset' in parameters:
        offset = parameters['offset']
        check_paging_value('offset', offset)
        query = query.offset(parameters['offset'])

    movies = query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)

    return jsonify({'movies': movies})


@app.route('/sfmovies/api/v1/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    """

    movie = MovieLocation.query.filter(
        MovieLocation.id == movie_id).first()
    if movie is None:
        raise InvalidUsage('No movie with id = ' + str(movie_id),
                           status_code=404,
                           payload={'links': [
                               {'href': '/api/v1/movies/' + str(movie_id),
                                'rel': 'self'}
                           ]})
    movie = jsonify_movie_location(movie)
    return jsonify({'movie': movie})

# ## Utility functions


def raise_invalid_parameter(parameter):
    """Raises an error when an invalid parameter is passed in the query string.

    Arguments:
    - `parameter`:
    """
    url = request.url
    api_index = url.index('/api/')
    url_suffix = urllib2.unquote(request.url[api_index:])
    raise InvalidUsage('Invalid parameter: {}'.format(parameter),
                       status_code=400,
                       payload={'links': [
                           {'href': url_suffix,
                            'rel': 'self'}]})


def check_paging_value(parameter, value):
    """Check that a paging value is an integer.

    Arguments:
    - `value`:
    """
    try:
        int(value)
    except:
        raise_invalid_parameter_value(parameter, value)


def check_field(field, properties):
    """Check that a field exists.

    Arguments:
    - `field`:
    - `properties`:
    """
    if field not in properties:
        raise_invalid_parameter_value('sort', field)


def check_parameter_name(parameter, value, properties):
    """Checks if a parameter name is valid, raises an error if this is not the
    case.

    Arguments:
    - `parameter`:
    - `value`:
    - `properties`:
    """
    if parameter not in properties:
        raise_invalid_parameter(parameter)

    if value == "":
        raise_invalid_parameter_value(parameter, "")

    if (parameter == 'id' or parameter == 'year'):
        try:
            int(value)
        except:
            raise_invalid_parameter_value(parameter, value)

    if (parameter == 'longitude' or parameter == 'latitude'):
        try:
            float(value)
        except:
            raise_invalid_parameter_value(parameter, value)


def raise_invalid_parameter_value(parameter, value):
    """Raises an error when an invalid parameter value is passed in the query
    string.

    Arguments:
    - `parameter`:
    - `value`:
    """
    url = request.url
    api_index = url.index('/api/')
    url_suffix = urllib2.unquote(request.url[api_index:])
    raise InvalidUsage('Invalid value: {},'.format(value) +
                       ' for parameter: {}'.format(parameter),
                       status_code=400,
                       payload={'links': [{
                           'href': url_suffix,
                           'rel': 'self'
                       }]})


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
