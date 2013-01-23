$(function() {

	// exists funct
	$.fn.exists = function () {
    	return this.length !== 0;
	}

	// arrows handler
     $(document).keydown(function(e){
		var LEFT_KEY = 37,
			UP_KEY = 38,
			RIGHT_KEY = 39;

		switch(e.keyCode) {
			case LEFT_KEY:
				if( $("#prev_page[href]").exists() )
					document.location = $("#prev_page").attr('href');
			break;

			case RIGHT_KEY:
				if( $("#next_page[href]").exists() )
					document.location = $("#next_page").attr('href');
			break;

			case UP_KEY:

			break;
		}
		e.preventDefault();
		return false;
	});
});