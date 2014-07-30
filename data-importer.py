#!/usr/bin/env python

# Quick and dirty script for importing all movie locations into app database.

# ## Imports

import sys
import json
from app import models
from app import db

# ## Script

def main():

  # Validate input
  if len(sys.argv) < 2:
    print "No JSON file specified, exiting script."
    return None

  filePath = sys.argv[1]

  # Read JSON file
  print "Reading JSON file"
  fileIn = open(filePath, 'r')
  movies = json.load(fileIn)
  fileIn.close()

  for movie in movies:

	# filter movies lacking minimum requirements for being interesting
	if 'locations' not in movie or 'title' not in movie \
	   or 'release_year' not in movie or 'latitude' not in movie \
	   or 'longitude' not in movie:
	  continue

	# Extract fields
	location = movie['locations']
	title = movie['title']
	year = int(movie['release_year'])
	latitude = movie['latitude']
	longitude = movie['longitude']

	fun_fact = movie['fun_facts'] if 'fun_facts' in movie else ""
	production_company = movie['production_company'] \
						 if 'production_company' in movie else ""
	distributor = movie['distributor'] if 'distributor' in movie else ""
	director = movie['director'] if 'director' in movie else ""
	writer = movie['writer'] if 'writer' in movie else ""
	actor_1 = movie['actor_1'] if 'actor_1' in movie else ""
	actor_2 = movie['actor_2'] if 'actor_2' in movie else ""
	actor_3 = movie['actor_3'] if 'actor_3' in movie else ""

	movieObj = models.MovieLocation(title = title,
									year = year,
									location = location,
									fun_fact = fun_fact,
									production_company = production_company,
									distributor = distributor,
									director = director,
									writer = writer,
									actor_1 = actor_1,
									actor_2 = actor_2,
									actor_3 = actor_3,
									latitude = latitude,
									longitude = longitude)

	print unicode(''+repr(movieObj), 'utf-8')

# ## Run script

main()
