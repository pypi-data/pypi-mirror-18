(function($) {

	if ($.ZTFY === undefined) {
		$.ZTFY = {};
	}

	$.ZTFY.captcha = {

		initCaptcha: function(element) {
			var source = $(element.target || element);
			var data = source.data();
			var now = new Date();
			var target = '@@captcha.jpeg?id=' + data.captchaId + unescape('%26') + now.getTime();
			source.attr('src', target)
				  .off('click')
				  .on('click', $.ZTFY.captcha.initCaptcha);
		}
	}

})(jQuery);
