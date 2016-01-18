var constructGeolocationLink = function constructGeolocationLink($wrapper){
    var geolocationIsSupported = true;

    if(geolocationIsSupported) {
        var t1 = $wrapper.attr('data-link-text') || 'Use my current location';
        var t2 = $wrapper.attr('data-loading-text') || 'Getting location\u2026';

        var $a = $('<a>').text(t1).addClass('geolocation-link');
        $a.on('click', function(){
            $(this).text(t2);
            setTimeout(function(){
                window.location.reload();
            }, 2000);
        })
        $a.appendTo($wrapper);
    }
}

$(function(){
    $('.js-geolocation-link').each(function(){
        constructGeolocationLink( $(this) );
    });
});
