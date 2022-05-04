/*======================================================

Project: Click To Call - Direct Call From Website HTML Plugin
Author: Black Theme
Released On: 8, Sep 2019
@version: 1.0 

========================================================*/

// to change fa icon of floating chat button
$(function() { 
    $("#cc-times").hide();
    $("#cc-phone").click(function() {
        $("#cc-phone").hide();
        $("#cc-times").fadeIn();
        $(".cc-panel").removeClass("animated bounceOutRight");
        $(".cc-panel").addClass("animated bounceInRight");
        $(".cc-panel").show();
    });

    $("#cc-times").click(function() {
        $("#cc-times").hide();
        $("#cc-phone").fadeIn();
        $(".cc-panel").removeClass("animated bounceInRight");               
        $(".cc-panel").addClass("animated bounceOutRight");
        //$(".cc-panel").hide();
    });

    $("#cc-close").in('click', function() {
        console.log('click');
        // $("#cc-times").hide();
        // $("#cc-phone").fadeIn();
        // $(".cc-panel").removeClass("animated bounceInRight");
        $(".cc-panel").addClass("animated bounceOutRight");
        //$(".cc-panel").hide();
    });
});

