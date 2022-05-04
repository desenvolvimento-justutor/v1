/*======================================================

Project: Click To Call - Direct Call From Website HTML Plugin
Author: Black Theme
Released On: 5, Sep 2019
@version: 1.0

========================================================*/

// to change fa icon of floating chat button
function clear() {
    $(".cc-panel").removeClass("animated");
    $(".cc-panel").removeClass("zoomOutUp");
    $(".cc-panel").removeClass("bounceInRight");
    $(".cc-panel").removeClass("zoomOutUp");
    $(".cc-panel").removeClass("shake");
}
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

    $("#cc-close").click(function() {
        clear();
        // $("#cc-times").hide();
        // $("#cc-phone").fadeIn();
        // $(".cc-panel").removeClass("animated bounceInRight");
        $.unblockUI();
        $(".cc-panel").addClass("animated bounceOutRight");
        // $(".cc-panel").hide();
    });
    $('[data-toggle="send"]').click(function (e) {
        clear();
        var elm = $(e.currentTarget);
        $('#input-pk').val(elm.data("pid"));
        $('.cc-user-img').attr('src', elm.data('image'));
        $('.cc-user-info').html(`<strong>${elm.data('nome')}</strong>`);
        $('body').block({ message: null, baseZ: 9980 });
        $(".cc-panel").removeClass("animated bounceOutRight");
        $(".cc-panel").addClass("animated bounceInRight");
        $("#cc-close").fadeIn();
        $(".cc-panel").show();
    });
    $('[data-toggle="send2"]').on('click', function (e) {
        clear();
        var elm = $(e.currentTarget);
        $('#cid').val(elm.data('cid'));
        $('#aid').val(elm.data('pk'));
        $('.cc-user-img').attr('src', elm.data('image'));
        $('.cc-user-info').html(`<strong>${elm.data('nome')}</strong>`);

        $('body').block({ message: null, baseZ: 9980 });
        $(".cc-panel").removeClass("animated bounceOutRight");
        $(".cc-panel").addClass("animated bounceInRight");
        $("#cc-close").fadeIn();
        $(".cc-panel").show();
    })
});