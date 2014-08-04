uber-coding-challenge
=====================

This project presents a solution to the SF Movies coding challenge.

SF Movies: Create a service that shows on a map where movies have been filmed in
San Francisco. The user should be able to filter the view using autocompletion
search.

- The project is hosted on [heroku](http://urbak-sfmovies.herokuapp.com/sfmovies/)
- The source code is located on
  [github](https://github.com/dragonwasrobot/uber-coding-challenge).
- Documentation of how to use the API is located at [API docs](http://urbak-sfmovies.herokuapp.com/sfmovies/api/v1/).

# Technical track

I've chosen the back-end track: include a minimal front-end (e.g. a static view,
API docs, etc. - do not spend time on it). Write, document and test your API as
if it will be used by other services and front-ends.

# Technology stack

- Language: Python (basic experience)
- Backend framework: Flask (no experience)
- Database: PostgreSQL (no experience)
- Frontend framework: None

## Reasoning:

**Language**: Having only had basic experience with Python and knowing that Uber
uses it as their language of choice for their back-end, I decided to jump into
the deep end of the pool and use a stack close to what Uber is currently using.

**Backend framework**: I chose Flask as the back-end framework as it seemed to
nicely fit the scale of the project while being very flexible and easy to set
up.

**Database**: While I have had experienced with different SQL databases, I
hadn't tried PostgreSQL before, so decided to use it as it is part of the Uber
stack (and works great if you want to deploy on Heroku).

**Frontend**: As the focus of this project is the back-end, the front-end has
been implemented as a single 'index.html' with an accompanying CSS and
JavaScript file.

# Design choices

Below, I go through some of the major design choices made in the process of
creating the project.

## Back-end

- Implemented the back-end as a REST service:
    - Client-server: A uniform interface separates clients from the servers,
      i.e., the API provided by the server.
    - Stateless: The server stores no client context.
    - Cacheable: The server sends a 'cache control' header with every response,
      and it also caches requests itself.
    - Layered system: The system is implemented such that no one layer can see
      past the next, which allows middleware to be added or removed as
      fitting.
    - Uniform interface: All resources are accessed via the URI:
      `/sfmovies/api/v1/movies/` and all results are represented using JSON,
      even error messages.
  - As such the API adheres to the above principles along with many of the best
    practices such as:
    - Using plural nouns for the resources.
    - HATEOAS: Adds hyperlinks to the JSON results for better navigation through
      the API (very simple though for this case).
    - Provides filtering, sorting, field selection and paging for resources.
    - Versioning of the API in the URL.
    - Error handling with HTTP status codes and error payloads also represented
      with JSON.
- However, implementing a truly RESTful service - including all best practices -
is non-trivial, so there are still a selection of minor tweaks one could make to
improve the service, as listed in
[Future optimizations](https://github.com/dragonwasrobot/uber-coding-challenge/issues/16),
which would also be the next issues to address if given more time.
- The back-end has been implemented in a TDD fashion, but could have been done
  more rigorously.
- The API Python code adheres to the PEP8 Style guide.
- The database schema used for the movie locations is very basic having just one
  table in which each row corresponds to a movie location. Potentially one could
  take more advantage of the relational structure and add tables for directors,
  writers, actors, etc. or alternatively go the opposite way and explore a
  schemaless approach instead.
- To make the data model of the application more flexible and extensible, I use
  a Python library for automatically handling database migration when changing
  the object models.

## Front-end

- The autocompletion search is only applied on the titles of the movies, but the
  API exposes resources that would allow us to extend the search to any field of
  a movie location object, e.g., 'writer, 'director' and 'actor_1'.
- Used the Google Maps API 3 to show the map and add the markers for every movie
  location.
- Used Google's Geocoding API to add latitude and longitude values for all movie
  locations.
- The JavaScript code has been checked with the JSHint tool.
