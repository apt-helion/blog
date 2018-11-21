(function($) {
    'use-strict';
    /* ---------------------------------------------- /*
     * Initialization general scripts for all pages
    /* ---------------------------------------------- */
    var scroll_to = $('a.scroll-to');

    /* ---------------------------------------------- /*
     * Strip pre tag whitespace
    /* ---------------------------------------------- */
    $.fn.prettyPre = function( method ) {

        var defaults = {
            ignoreExpression: /\s/ // what should be ignored?
        };

        var methods = {
            init: function( options ) {
                this.each( function() {
                    var context = $.extend( {}, defaults, options );
                    var $obj = $( this );
                    var usingInnerText = true;
                    var text = $obj.get( 0 ).innerText;

                    // some browsers support innerText...some don't...some ONLY work with innerText.
                    if ( typeof text == "undefined" ) {
                        text = $obj.html();
                        usingInnerText = false;
                    }

                    // use the first line as a baseline for how many unwanted leading whitespace characters are present
                    var superfluousSpaceCount = 0;
                    var currentChar = text.substring( 0, 1 );

                    while ( context.ignoreExpression.test( currentChar ) ) {
                        currentChar = text.substring( ++superfluousSpaceCount, superfluousSpaceCount + 1 );
                    }

                    // split
                    var parts = text.split( "\n" );
                    var reformattedText = "";

                    // reconstruct
                    var length = parts.length;
                    for ( var i = 0; i < length; i++ ) {
                        // cleanup, and don't append a trailing newline if we are on the last line
                        reformattedText += parts[i].substring( superfluousSpaceCount ) + ( i == length - 1 ? "" : "\n" );
                    }

                    // modify original
                    if ( usingInnerText ) {
                        $obj.get( 0 ).innerText = reformattedText;
                    }
                    else {
                        // This does not appear to execute code in any browser but the onus is on the developer to not
                        // put raw input from a user anywhere on a page, even if it doesn't execute!
                        $obj.html( reformattedText );
                    }
                } );
            }
        }

        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ) );
        }
        else if ( typeof method === "object" || !method ) {
            return methods.init.apply( this, arguments );
        }
        else {
            $.error( "Method " + method + " does not exist on jQuery.prettyPre." );
        }
    }
    $(document).ready(function($) {
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
                    }, 1000);
                }
                event.preventDefault();
            });
        }

        /* ---------------------------------------------- /*
         * Pre tag whitespace
        /* ---------------------------------------------- */
        $( function() { $("PRE").prettyPre(); } );
    });
})(jQuery);
