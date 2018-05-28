(function($) {
    'use-strict';
    /* ---------------------------------------------- /*
     * Initialization general scripts for all pages
    /* ---------------------------------------------- */
    var mobile_test = '',
        highlight_post = $('.highlight-post'),
        instafeed = $('#instafeed'),
        instafeed_user_id = $('#instafeed').data('user-id'),
        instafeed_access_token = $('#instafeed').data('access-token'),
        instafeed_amount = parseInt($('#instafeed').data('amount')),
        scroll_to = $('a.scroll-to'),
        map = $('#googlemaps'),
        gm_address = $('#googlemaps').data('address'),
        gm_center_lat = parseFloat($('#googlemaps').data('lat')),
        gm_center_long = parseFloat($('#googlemaps').data('long')),
        gm_zoom = parseInt($('#googlemaps').data('zoom')),
        is_draggable = Math.max($(window).width(), window.innerWidth) > 480 ? true : false,
        product_slider = $('ul.product-slider.light-slider'),
        gallery_slider = $('ul.gallery-slider.light-slider'),
        comment_form_wrapper = $('#comment-form'),
        comment_list_wrapper = $('.comment-list-wrapper'),
        comment_preview_btn = $('#comment-form #btn-preview'),
        comment_name_input_wrapper = $('#comment-form .name-input-wrapper'),
        comment_email_input_wrapper = $('#comment-form .email-input-wrapper'),
        comment_website_input_wrapper = $('#comment-form .website-input-wrapper'),
        comment_name_input_field = comment_name_input_wrapper.find('input.name')
        comment_input_field = $('#comment-form textarea.comment');
    /* ---------------------------------------------- /*
     * Mobile detect
    /* ---------------------------------------------- */
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        mobileTest = true;
    } else {
        mobileTest = false;
    }
    $(document).ready(function($) {
        /* ---------------------------------------------- /*
         * Parallax
        /* ---------------------------------------------- */
        if (highlight_post.length > 0) {
            $(window).resize(function() {
                highlight_post.parallax('50%', 0.1, true);
            });
        }
        /* ---------------------------------------------- /*
         * Instafeed
        /* ---------------------------------------------- */
        if (instafeed.length > 0) {
            instafeed.empty();
            var feed = new Instafeed({
                limit: instafeed_amount,
                sortBy: 'most-recent',
                resolution: 'standard_resolution',
                get: 'user',
                userId: instafeed_user_id,
                accessToken: instafeed_access_token,
                template: '<li><a href="{{link}}" class="instafeed-thumbnail" target="_blank"><img id="{{id}}" src="{{image}}" class="img-responsive" alt="{{caption}}" /></a></li>'
            });
            feed.run();
        }
        /* ---------------------------------------------- /*
         * Display comment form fields on focus
        /* ---------------------------------------------- */
        if (comment_form_wrapper.length > 0) {
            if (comment_input_field.length > 0) {
                comment_input_field.one('click', function() {
                    comment_name_input_wrapper.delay(100).slideDown('fast');
                    comment_email_input_wrapper.delay(150).slideDown('fast');
                    comment_website_input_wrapper.delay(200).slideDown('fast');
                });
            }
        }
        /* ---------------------------------------------- /*
         * Update comment preview on click and keyup
        /* ---------------------------------------------- */
        if (comment_list_wrapper.length > 0 && comment_preview_btn.length > 0) {
            comment_preview_btn.one('click', function() {
                var author = comment_name_input_field,
                    comment = (comment_input_field.val()) ? comment_input_field.val() : '...',
                    comment_markup = '';
                author = (author.val()) ? author.val() : 'Not Logged In'
                comment_markup = '<div id="comment-prev" class="comment clearfix">';
                comment_markup += '<div class="comment-avatar"><img src="default-avatar.png" class="img-responsive" /></div>';
                comment_markup += '<div class="comment-content clearfix">';
                comment_markup += '<div class="comment-author"><a href="#">' + author + ' </a></div>';
                comment_markup += '<div class="comment-entry">';
                comment_markup += '<p>' + comment + '</p>';
                comment_markup += '</div>';
                comment_markup += '<div class="comment-meta"><span>Just now</span></div>';
                comment_markup += '</div>';
                comment_markup += '</div>';
                comment_list_wrapper.prepend(comment_markup);
                $('#comment-prev').fadeIn('fast');
            });
            // Update preview comment author name on keyup
            comment_name_input_field.keyup(function() {
                var author = ($(this).val()) ? $(this).val() : 'Not Logged In';
                $('#comment-prev .comment-author a').text(author);
            });
            // Update preview comment message on keyup
            comment_input_field.keyup(function() {
                var comment = ($(this).val()) ? $(this).val() : '...';
                $('#comment-prev .comment-entry p').text(comment);
            });
        }
        /* ---------------------------------------------- /*
         * Smooth scroll to section or div
        /* ---------------------------------------------- */
        if ($(scroll_to).length > 0) {
            $(scroll_to).click(function(event) {
                var target = '#';
                target += $(this).data('scroll-to');
                if ($(target).length > 0) {
                    $('html, body').animate({
                        scrollTop: $(target).offset().top
                    }, 2000);
                }
                event.preventDefault();
            });
        }
        /* ---------------------------------------------- /*
         * Google Maps iframe embed disable scroll to zoom
        /* ---------------------------------------------- */
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
        /* ---------------------------------------------- /*
         * Light slider with carousel products navigation
        /* ---------------------------------------------- */
        if (product_slider.length > 0) {
            setTimeout(function() {
                product_slider.lightSlider({
                    auto: false,
                    item: 4,
                    loop: false,
                    slideMove: 2,
                    slideMargin: 30,
                    easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
                    speed: 600,
                    galleryMargin: 36,
                    prevHtml: '<i class="fa fa-long-arrow-left"></i>',
                    nextHtml: '<i class="fa fa-long-arrow-right"></i>',
                    responsive: [{
                        breakpoint: 800,
                        settings: {
                            item: 3,
                            slideMove: 1,
                            slideMargin: 6,
                        }
                    }, {
                        breakpoint: 768,
                        settings: {
                            item: 2,
                            slideMove: 1
                        }
                    }]
                });
            }, 1000);
        }
        /* ---------------------------------------------- /*
         * Light slider with carousel thumbnails navigation
        /* ---------------------------------------------- */
        if (gallery_slider.length > 0) {
            setTimeout(function() {
                gallery_slider.lightSlider({
                    auto: false,
                    gallery: true,
                    item: 1,
                    loop: true,
                    thumbItem: 7,
                    slideMargin: 0,
                    enableDrag: true,
                    currentPagerPosition: 'left',
                    controls: false,
                    pauseOnHover: true,
                    adaptiveHeight: true,
                    galleryMargin: -30
                });
            }, 1000);
        }
    });
})(jQuery);