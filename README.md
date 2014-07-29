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

- I've chosen to jump into the deep end of the pool and use a range of
  technologies that I haven't used before to write anything production ready
  (which is also reflected in the experience listed for each technology).
- Since the focus of this application is on the backend, minimal work has been
  put into making it compatible with older browser versions and vendors.
- Likewise, only manual testing has been done of the frontend of the
  application.
- The whole backend is implemented using Test-driven development.
- Used the Google geocoding service to obtain coordinates for each movie
  location.
- Currently doing filtering of results on the client-side, this should be moved
  to the server for the sake of scalability.
