/* locations.js */

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
        content : contentString
    });

    // Add markers
    addMarkers(map, infowindow);
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

var addMarkers = function(map, infowindow) {

    var BASE_URL = "http://localhost:5000/sfmovies/api/";
    $.getJSON(BASE_URL + "v1.0/movies", function(data) {

        var movies = data.movies;
        for (var i = 0; i < movies.length; i++) {

            movie = movies[i];
            var markerContent = '<div id="content">' +
                '<h1>' + movie.title + '</h1>' +
                '<p><b>' + movie.title + '</b>' +
                ' (' + movie.release_year + ')' +
                ' was written by ' + movie.writer +
                ' and directed by ' + movie.director +
                ' and starred ' + movie.actor_1 +
                ' id: ' + movie.id +
                '</p></div>';

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
