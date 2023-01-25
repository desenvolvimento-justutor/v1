$(function(){
	// Initialize iCheck
  $('input').iCheck({
    checkboxClass: 'icheckbox_flat-purple',
    radioClass: 'iradio_flat-purple'
  });

  // Initialize Bootstrap Popover
  $('[data-toggle="popover"]').popover({
  	placement: 'auto',
  	html: true,
  	trigger: 'click'
  });

  // Initialize Bootstrap Tooltip
  $('[data-toggle="tooltip"]').tooltip({
  	container: 'body',
  	zIndex: 2002
  });

  // Clickable element with attribute data-href
  $("[data-href]").each(function() {
  	$(this).click(function() {
  		try {
	  		if(eval($(this).data('href'))){
		  		document.location = eval($(this).data('href'));
		  		return;
	  		}
  		} catch($e) {
	  		document.location = $(this).data('href');
  		}

  	});
  });

  // Trigger element to fadeIn or fadeOut
  $("[data-fade]").each(function() {
  	$(this).click(function() {
  		var $sel = $(this).data("fade"),
  				$in = $sel.split(",")[0],
  				$out = $sel.split(",")[1];

  		if($in) {
		  	$($in).fadeIn();
  		}
  		if($out) {
		  	$($out).fadeOut();
  		}
	  	return false;
  	});
  });

  // Trigger element to slideDown or slideUp
  $("[data-slide]").each(function() {
  	$(this).click(function() {
  		var $sel = $(this).data("slide"),
  				$in = $sel.split(",")[0],
  				$out = $sel.split(",")[1];

			if($(this).data("active")) {
		  		$($(this).data("active")).toggleClass("active");
			}

  		if($in) {
		  	$($in).slideToggle();
  		}
  		if($out) {
		  	$($out).slideToggle();
  		}
	  	return false;
  	});
  });

  $("[data-shipping-method]").each(function() {
  	$(this).click(function() {
  		$("[data-shipping-method]").removeClass("active");
  		$(this).addClass("active");
  		setShipping($(this).find("input:radio").val());
  	});
  });

  $(".payment-method-item").each(function() {
  	$(this).click(function() {
  		$(".payment-method-item").removeClass("active");
  		$(this).addClass("active");

  		$(".payment-method-form").removeClass('show').hide();
  		$("#" + $(this).data("target")).fadeIn();
  		$('button[name=confirmar]').val($(this).data("target"));
  		var payment_method = $(this).data("toggle");
  		console.log(payment_method);
  		$("input[name=paymentmethod]").val(payment_method);
		if (payment_method === 'creditcard') {
			$('#containner-parcelas').show();
			$('#creditcard-containner').show();
			$('#row-nome').hide();
			$('#payment_method_title').html('Cartão de Credito');
		} else if (payment_method === 'pix') {
			$('#containner-parcelas').hide();
			$('#creditcard-containner').hide();
			$('#row-nome').show();
			$('#payment_method_title').html('PIX');
		} else {
			$('#containner-parcelas').hide();
			$('#creditcard-containner').hide();
			$('#row-nome').show();
			$('#payment_method_title').html('Boleto');
		}
		$("#formCreditCard").validate().resetForm();
  	});
  });
	$("#helpme .helpme-inner").click(function() {
		let $this = $(this);

		if(!$(".helpme").hasClass("active")) {
			$(".helpme").addClass("active");
			$(".helpme-content-scrollable").niceScroll({
				cursoropacitymin: .3,
				cursoropacitymax: .8
			});
			$(".helpme input").focus();
			$("body").append($("<div>", {
				class: 'backdrop'
			}));
		}else{
			$("#helpme").removeClass("active");
			$(".backdrop").remove();
		}
	});

	$('header.primary').scrollupbar();
	if($(window).outerWidth() >= 1024) {	
		$(".navbar-secondary .navbar-inner").niceScroll({
			cursoropacitymax: .8
		});
	}
});
