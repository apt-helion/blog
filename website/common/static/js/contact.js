(function($) {
    'use-strict';
    /* ---------------------------------------------- /*
     * Initialization general scripts for all pages
    /* ---------------------------------------------- */
    var map = $('#googlemaps'),
        gm_address = $('#googlemaps').data('address'),
        gm_center_lat = parseFloat($('#googlemaps').data('lat')),
        is_draggable = Math.max($(window).width(), window.innerWidth) > 480 ? true : false,
        gm_center_long = parseFloat($('#googlemaps').data('long')),
        gm_zoom = parseInt($('#googlemaps').data('zoom'));

    $(document).ready(function($) {
        if (map.length > 0) {
            map.gmap3({
                zoom: gm_zoom,
                center: [gm_center_lat, gm_center_long],
                address: gm_address,
                zoomControl: true,
                zoomControlOptions: {
                    style: google.maps.ZoomControlStyle.SMALL
                },
                mapTypeControl: false,
                scaleControl: false,
                scrollwheel: false,
                streetViewControl: false,
                draggable: is_draggable,
                styles: [{
                    stylers: [{
                        hue: '#c8cccf'
                    }, {
                        saturation: -250
                    }]
                }, {
                    featureType: 'road',
                    elementType: 'geometry',
                    stylers: [{
                        lightness: 100
                    }, {
                        visibility: 'simplified'
                    }]
                }, {
                    featureType: 'road',
                    elementType: 'labels',
                    stylers: [{
                        visibility: 'off'
                    }]
                }]
            });
        }
    });
})(jQuery);
