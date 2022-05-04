/*=================================================

Project: Click To Call - Direct Call From Website HTML Plugin
Author: Black Theme
Released On: 8, Sep 2019
@version: 1.0

===================================================*/

// On Page Load Function
$(document).ready(function(){

    // Disable Keybord Key Event
    // document.onkeydown = function (e)
    // {
    //     //alert();
    //     return false;
    // }
    
    // Disable Mouse Key Event
    // document.oncontextmenu = document.body.oncontextmenu = function() {return false;}

	// START NEW SECTION 1 JS
	// Class Color Click Event Function
	$(".color1" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-black.css");
		return false;
	});

	$(".color2" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-blue.css");
		return false;
	});

	$(".color3" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-green.css");
		return false;
	});

	$(".color4" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-orange.css");
		return false;
	});

	$(".color5" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-pink.css");
		return false;
	});
		
	$(".color6" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-purple.css");
		return false;
	});

	$(".color7" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-red.css");
		return false;
	});

	$(".color8" ).click(function(){
		$("#call-color" ).attr("href", "css/colors/color-yellow.css");
		return false;
	});

	// Click To Call Slider Function 
	$('.icon').click (function(event){
		event.preventDefault();
		if( $ (this).hasClass('inOut')  ){
			$('.cc-setting').stop().animate({left:'-210px'},500 );
		} else{
			$('.cc-setting').stop().animate({left:'0px'},500 );
		} 
		$(this).toggleClass('inOut');
		return false;

	});
	// END NEW SECTION 1 JS

	// START NEW SECTION 2 JS
	// For the dropdown menu under the Click To Call Style 10
    
    var countOption = $('.old-select option').size();
    
    function openSelect(){
        var heightSelect = $('.new-select').height();
        var j=1;
        $('.new-select .new-option').each(function(){
            $(this).addClass('reveal');
            $(this).css({
                'box-shadow':'0 1px 1px rgba(0,0,0,0.1)',
                'left':'0',
                'right':'0',
                'top': j*(heightSelect+1)+'px'
            });
            j++;
        });
    }
    
    function closeSelect(){
        var i=0;
        $('.new-select .new-option').each(function(){
            $(this).removeClass('reveal');
            if(i<countOption-3){
                $(this).css('top',0);
                $(this).css('box-shadow','none');
            }
            else if(i===countOption-3){
                $(this).css('top','3px');
            }
            else if(i===countOption-2){
                $(this).css({
                    'top':'7px',
                    'left':'2px',
                    'right':'2px'
                });
            }
            else if(i===countOption-1){
                $(this).css({
                    'top':'11px',
                    'left':'4px',
                    'right':'4px'
                });
            }
            i++;
        });
    }
    
    // Initialisation
    if($('.old-select option[selected]').size() === 1){
        $('.selection p span').html($('.old-select option[selected]').html());
    }
    else{
        $('.selection p span').html($('.old-select option:first-child').html());
    }
    
    $('.old-select option').each(function(){
        newValue = $(this).val();
        newHTML = $(this).html();
        $('.new-select').append('<div class="new-option" data-value="'+newValue+'"><p>'+newHTML+'</p></div>');
    });
    
    var reverseIndex = countOption;
    $('.new-select .new-option').each(function(){
        $(this).css('z-index',reverseIndex);
        reverseIndex = reverseIndex-1;        
    });
    
    closeSelect();

    // Ouverture / Fermeture
    $('.selection').click(function(){
        $(this).toggleClass('open');
        if($(this).hasClass('open')===true){openSelect();}
        else{closeSelect();}
    });
 
    $('.cc-button2').hide();
    $('.cc-button3').hide();
    $('.cc-button4').hide();
    $('.cc-button5').hide();
    $('.cc-button6').hide();
    $('.cc-button7').hide();
    // Selection 
    $('.new-option').click(function(){
        var newValue = $(this).data('value');

        $('.cc-button1').hide();
        $('.cc-button2').hide();
        $('.cc-button3').hide();
        $('.cc-button4').hide();
        $('.cc-button5').hide();
        $('.cc-button6').hide();
        $('.cc-button7').hide();

        if(newValue == 'cc-style1'){
        	$('.cc-button1').fadeIn();
        }
        else if(newValue == 'cc-style2'){
        	$('.cc-button2').fadeIn();
        }
        else if(newValue == 'cc-style3'){
        	$('.cc-button3').fadeIn();
        }
        else if(newValue == 'cc-style4'){
        	$('.cc-button4').fadeIn();
        }
        else if(newValue == 'cc-style5'){
        	$('.cc-button5').fadeIn();
        }
        else if(newValue == 'cc-style6'){
        	$('.cc-button6').fadeIn();
        }
        else if(newValue == 'cc-style7'){
        	$('.cc-button7').fadeIn();
        }

        // Selection New Select
        $('.selection p span').html($(this).find('p').html());
        $('.selection').click();
        
        // Selection Old Select
        $('.old-select option[selected]').removeAttr('selected');
        $('.old-select option[value="'+newValue+'"]').attr('selected','');
   
    });
    
	// END NEW SECTION 2 JS
	
	// START NEW SECTION 3 JS
	// Whats Style Screen Shotes Image Hover Effect
 
    $(".cc-zoom").hover(function(){
        
        $(this).addClass('transition');
    }, function(){
        
        $(this).removeClass('transition');
    });
	// END NEW SECTION 3 JS	
});
