uber-coding-challenge
=====================

Shows locations of movies filmed in San Francisco

# Problem description

Create a service that shows on a map where movies have been filmed in San
Francisco. The user should be able to filter the view using autocompletion
search.

# Technical track

I've chosen the back-end track: include a minimal front-end (e.g. a static view,
API docs, etc. - do not spend time on it). Write, document and test your API as
if it will be used by other services and front-ends.

Note: The front-end is not completely minimal but does provides an appropriate
level of functionality and interaction to reflect the project solution.

# Technology stack

- Language: Python (basic experience)
- Database: PostgreSQL (no experience)
- Backend framework: Flask (no experience)
- Caching layer: Memcached (no experience)
- Frontend framework: None
- Map visualization: Google maps (basic experience)

# Design choices

## General

- I've chosen to jump into the deep end of the pool and use a range of
  technologies that I haven't used before to write anything production ready
  (which is also reflected in the experience listed for each technology).

## Front-end

- The autocompletion search is only applied on the titles of the movies, but the
  API exposes resources that would allow us to extend the search to any field of
  a movie location object, e.g., 'writer, 'director' and 'actor_1'.
- As the focus is on the back-end, little focus has been put on:
  - automatic testing.
  - backwards compatible and consistency across vendors.
  - writing perfect code.
- Used the Google Maps API 3 to show the map and add the markers for every movie
  location.
- The JavaScript code checked with the JSHint tool.

## Back-end

- Flask: minimal framework for backend Python.

- Implemented the back-end as a REST service:
  - Client-server: A uniform interface separates clients from the servers, i.e.,
    the API provided by the server.
  - Stateless: The server stores no client context.
  - Cacheable: The server sends a 'cache control' header with every response,
    and it also caches requests itself.
  - Layered system: The system is implemented such that no one layer can see
    past the next, which allows middleware to be added or removed as
    fitting. For example, we may easily introduce a caching layer without it
    affecting the client.
  - Uniform interface: All resources are accessed via the URI:
    `/sfmovies/api/v1/movies/` and all results are represented using JSON.

  - Content negotiation: Only supports "Content-type: application/json"

- Wrote the REST part from scratch but could potentially have used the
  flask-restful
- The back-end is very restrictive as it only allows GET requests as there is no
  authentication mechanism to allow POST, PUT and DELETE to happen in a
  responsible manner.
- It is also slacking a bit on the HATEOAS requirements of the REST principles.

- Implemented in a test-driven fashion, but not in the completely rigorous way.
- Used the Google geocoding service to obtain coordinates for each movie
  location.
- Python code adheres to the PEP8 Style guide.

- PostgreSQL: A basic structure where one movie location record is translated
  into one row in a table.
  - Possible improvement: Take more advantage of the relational structure by
    adding tables for 'director', 'writer', etc., if needed.
- Database migration: To make the application more flexible and extensible, we
  use a Python library for automatically handling database migration when
  changing the object 'model'.
