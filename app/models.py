# models.py

# ## Imports

from app import db

# ## Models

class MovieLocation(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(80), index = True)
  release_year = db.Column(db.Integer, index = True)
  locations = db.Column(db.String(128))
  fun_facts = db.Column(db.String(512))
  production_company = db.Column(db.String(80), index = True)
  distributor = db.Column(db.String(80), index = True)
  director = db.Column(db.String(80), index = True)
  writer = db.Column(db.String(80), index = True)
  actor_1 = db.Column(db.String(80), index = True)
  actor_2 = db.Column(db.String(80), index = True)
  actor_3 = db.Column(db.String(80))
  latitude = db.Column(db.Float())
  longitude = db.Column(db.Float())

  def __init__(self, title, release_year, locations, fun_facts,
               production_company, distributor, director, writer,
               actor_1, actor_2, actor_3, latitude, longitude):
    """
    """
    self.title = title
    self.release_year = release_year
    self.locations = locations
    self.fun_facts = fun_facts
    self.production_company = production_company
    self.distributor = distributor
    self.director = director
    self.writer = writer
    self.actor_1 = actor_1
    self.actor_2 = actor_2
    self.actor_3 = actor_3
    self.latitude = latitude
    self.longitude = longitude

  def __repr__(self):
    return '<MovieLocation: {} ({}), written by {} and directed by: {}>'.format(
      self.title, self.release_year, self.writer, self.director)
