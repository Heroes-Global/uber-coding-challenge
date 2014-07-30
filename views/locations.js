/* locations.js */

// # Constants
var BASE_URL = "http://localhost:5000/sfmovies/api/";

// # Functions

// Initialize front end
var initialize = function() {

    // Initialize map
    var MAP_CANVAS = "map-canvas";
    var SF_LATITUDE = 37.748;
    var SF_LONGITUDE = -122.429;
    var DEFAULT_ZOOM = 13;

    var mapOptions = {
        center : new google.maps.LatLng(SF_LATITUDE, SF_LONGITUDE),
        zoom : DEFAULT_ZOOM
    };

    var map = new google.maps.Map(document.getElementById(MAP_CANVAS),
                                  mapOptions);

    // Initialize Info window
    var contentString = "<placeholder text>";

    infowindow = new google.maps.InfoWindow({
        content : contentString,
				maxWidth: 300,
    });

    // Initialize Search box
    var searchBar = document.getElementById('search-bar');
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(searchBar);

    $("#movie-input").autocomplete({
        delay : 300,
        appendTo : "#search-bar",
        minLength: 2,
        source : function(request, response) {
            $.getJSON(BASE_URL + "v1.0/titles", function(data) {
                term = request.term;
                titles = $.grep(data.titles, function(title) {
                    return title.toLowerCase().indexOf(term.toLowerCase()) > -1;
                });
                if (titles.length > 5) {
                    titles = titles.slice(0,5);
                }
                response(titles);
            });
        },
    });

    $("#movie-input").keypress(function(event) {

        if (event.keyCode == 13) {
            var titles = [];
            $.each($('.ui-menu-item'), function() {
                titles.push($(this).text());
            });
            var input = $("#movie-input").val();

            queryTitle = $('.ui-menu-item').first().text();

            for (var i = 0; i < titles.length; i++) {
                var title = titles[i];
                if (title.toLowerCase() === input.toLowerCase()) {
                    queryTitle = title;
                    break;
                }
            }

            // Set search title and add markers
            $("#movie-input").val(queryTitle);
            clearMarkers();
            addMarkers(queryTitle, map, infowindow);
        }

    });

};

// Initialize markers
var markers = [];

var clearMarkers = function() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;
};

var addMarkerClickListener = function(map, marker) {
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(marker.data);
        infowindow.open(map, marker);
    });
};

var addMarkers = function(title, map, infowindow) {

    $.getJSON(BASE_URL + "v1.0/movies?title=" + title, function(data) {

        var movies = data.movies;
        for (var i = 0; i < movies.length; i++) {

            movie = movies[i];

            if (movie.title !== title) {
                continue;
            }

						// Determine marker content based on the format of the movie data.
						var markerContent = '<div id="content">' +
                '<h1>' + movie.title + '</h1>' +
                '<p><b>' + movie.title + '</b>' +
                ' (' + movie.year + ')';

						if (movie.writer == movie.director) {
								markerContent += ' was written and directed by <b>' +
										movie.director + '</b>.';
						} else {
								markerContent += ' was written <b>' + movie.writer +
										'</b> and directed by <b>' + movie.director + '</b>.';
						}

						if (movie.actor_1 !== '') {
								markerContent += ' It starred <b>' + movie.actor_1 + '</b>';
								if (movie.actor_2 !== '') {
										markerContent += ' and <b>' + movie.actor_2 + '</b>';
								}
								markerContent += ".";
						}

						// Create marker
            var marker = new google.maps.Marker({
                position : new google.maps.LatLng(movie.latitude,
                                                  movie.longitude),
                map : map,
                data : markerContent
            });

            markers.push(marker);
            addMarkerClickListener(map, marker);
        }
    });
};

google.maps.event.addDomListener(window, 'load', initialize);
