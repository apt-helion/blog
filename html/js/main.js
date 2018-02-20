$(document).ready(function() {

	$('#show-btn').click(function() {
		$('#tree').slideToggle();
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

});
