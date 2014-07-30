#!/usr/bin/env python

# Quick and dirty script for getting the max lengths of the different object
# properties as a hint for how large each of the table columns in the database
# should be.

# # Imports

import sys
import json

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

    # Get max lengths
    title_length = 0
    release_year_length = 0
    locations_length = 0
    fun_facts_length = 0
    production_company_length = 0
    distributor_length = 0
    director_length = 0
    writer_length = 0
    actor_1_length = 0
    actor_2_length = 0
    actor_3_length = 0
    latitude_length = 0
    longitude_length = 0

    for movie in movies:

        keys = movie.keys()

        if 'title' in keys and
        len(movie['title']) > title_length:
            title_length = len(movie['title'])

        if 'release_year' in keys and
        len(movie['release_year']) > release_year_length:
            release_year_length = len(movie['release_year'])

        if 'locations' in keys and
        len(movie['locations']) > locations_length:
            locations_length = len(movie['locations'])

        if 'fun_facts' in keys and
        len(movie['fun_facts']) > fun_facts_length:
            fun_facts_length = len(movie['fun_facts'])

        if 'production_company' in keys and
        len(movie['production_company']) > production_company_length:
            production_company_length = len(movie['production_company'])

        if 'distributor' in keys and
        len(movie['distributor']) > distributor_length:
            distributor_length = len(movie['distributor'])

        if 'director' in keys and
        len(movie['director']) > director_length:
            director_length = len(movie['director'])

        if 'writer' in keys and
        len(movie['writer']) > writer_length:
            writer_length = len(movie['writer'])

        if 'actor_1' in keys and
        len(movie['actor_1']) > actor_1_length:
            actor_1_length = len(movie['actor_1'])

        if 'actor_2' in keys and
        len(movie['actor_2']) > actor_2_length:
            actor_2_length = len(movie['actor_2'])

        if 'actor_3' in keys and
        len(movie['actor_3']) > actor_3_length:
            actor_3_length = len(movie['actor_3'])

    # Print results
    print "title_length: " + str(title_length)
    print "release_year_length: " + str(release_year_length)
    print "locations_length: " + str(locations_length)
    print "fun_facts_length: " + str(fun_facts_length)
    print "production_company_length: " + str(production_company_length)
    print "distributor_length: " + str(distributor_length)
    print "director_length: " + str(director_length)
    print "writer_length: " + str(writer_length)
    print "actor_1_length: " + str(actor_1_length)
    print "actor_2_length: " + str(actor_2_length)
    print "actor_3_length: " + str(actor_3_length)

# # Run script

main()
