$(document).ready(function() {

	$('#show-btn').click(function() {
		if ($(window).width() < 1000) {
			$('.cTree').slideToggle();
		}
	});

	$('#blink').each(function() {
		var elem = $(this);
		setInterval(function() {
			if (elem.css('visibility') == 'hidden') {
				elem.css('visibility', 'visible');
			} else {
				elem.css('visibility', 'hidden');
			}
		}, 500);
	});

	$(window).on('resize', function () {
		var win = $(this);
		if (win.width() >= 1000) {
			$('.cTree').show();
		}
	});

});
