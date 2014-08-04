#!/usr/bin/env python

# Quick and dirty script for augmenting a list of movie locations with their
# respective coordinates (latitude, longitude) using Google's geocoding API.

# # Imports

import sys
import json
import urllib2
from time import sleep
from config import SERVER_KEY

# # Script


def main():
    """Reads a JSON file containing movie locations and augments each of the
    locations with a longitude and latitude property.

    """

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

    # Perform geocoding
    print "Performing requests"
    counter = 0
    for movie in movies:
        print "Entry: " + counter
        if 'locations' not in movie.keys():
            counter += 1
            continue

        encodedLocation = urllib2.quote(movie['locations'].encode("utf8"))
        requestUrl = "https://maps.googleapis.com/maps/api/geocode/" + \
					 "json?address=" + encodedLocation + \
									 ",+San+Francisco,+CA&key=" + SERVER_KEY
        print requestUrl
        jsonResponse = json.load(urllib2.urlopen(requestUrl))

        if len(jsonResponse['results']) > 0:
            coordinates = jsonResponse['results'][0]['geometry']['location']
            movie['latitude'] = coordinates['lat']
            movie['longitude'] = coordinates['lng']
            print movie

        counter += 1
        sleep(0.1)

    # Write augmented JSON file
    print "Writing output"
    outPath = "out.json"
    if len(sys.argv) > 2:
        outPath = sys.argv[2]
    fileOut = open(outPath, 'w')
    json.dump(movies, fileOut)
    fileOut.close()
    print "Output written to: " + outPath

    print "Script exited successfully"

# # Run script

main()
