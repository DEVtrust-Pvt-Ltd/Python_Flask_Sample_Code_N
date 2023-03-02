/* Start: Fix Header */
	$(window).scroll(function() {     
		var scroll = $(window).scrollTop();
		if (scroll > 10) {
			$("#header").addClass("active");
		}
		else {
			$("#header").removeClass("active");
		}
	});
/* End: Fix Header */


/*Start: Back to Top */
$(window).scroll(function () {
	if ($(this).scrollTop() > 450) {
		$('#scrollTop').fadeIn();
	} else {
		$('#scrollTop').fadeOut();
	}
});
// scroll up function
$('#scrollTop').click(function () {
	$('html, body').animate({ scrollTop: 0 }, 450);
});
/*End: Back to Top */


