/*======================================================

Project: Click To Call - Direct Call From Website HTML Plugin
Author: Black Theme
Released On: 8, Sep 2019
@version: 1.0

========================================================*/

$(document).ready(function(){

    /* Click To Call Sidebar Function */
    $('.cc-button').click (function(event){
        
        event.preventDefault();
        
        if( $ (this).hasClass('inOut') ){
            $('.cc-style3').stop().animate({right:'-260px'},500 );

        }else{
            $('.cc-style3').stop().animate({right:'0px'},500 );
        } 

        $(this).toggleClass('inOut');

        return false;

    });
});

