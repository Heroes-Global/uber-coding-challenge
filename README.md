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

# Technology stack

- Language: Python (basic experience)
- Backend framework: Flask (no experience)
- Frontend framework: None
- Map visualization: Google maps (basic experience)
- Database: PostgreSQL (no experience)

# Design choices

## General

- I've chosen to jump into the deep end of the pool and use a range of
  technologies that I haven't used before to write anything production ready
  (which is also reflected in the experience listed for each technology).

## Front-end

- The autocompletion search is only applied on the titles of the movies.
  - Possible extension: Make fields like 'writer, 'director' and 'actor'
    searchable.
- We presume in the autocompletion that no two movies with the same 'title' has
  been shot in San Francisco.
  - Improvement: Filter on both 'title' and 'year'.
- As the focus is on the backend, there is no automatic testing of the
  front-end.
- Likewise, minimal has been done to make the front-end backwards compatible and
  consistent across vendors.
- (Something about filtering on the client vs server side).
- Used the Google Maps API 3 to show the map and add the markers for every movie
  location.

## Back-end

- Implemented in a test-driven fashion, but not done in the completely rigorous
  way.
- Used the Google geocoding service to obtain coordinates for each movie
  location.

### API

- Flask: minimal framework for backend Python.

### Database

- PostgreSQL: A basic structure where one movie location record is translated
  into one row in a table.
  - Possible improvement: Take more advantage of the relational structure by
    adding tables for 'director', 'writer', etc., if needed.
- Database migration: To make the application more flexible and extensible, we
  use a Python library for automatically handling database migration when
  changing the object 'model'.
