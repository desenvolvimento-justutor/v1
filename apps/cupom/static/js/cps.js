(function ($) {
    $(function () {
        addBtn();
        var $tipo = $('#id_tipo');
        $tipo.change(function () {
            selecionaForm()
        });
        selecionaForm();

        $('form').on('click', '#btn-gerar-codigo', function () {
            $('#id_codigo').val(makeid(6));
        });
    });
    var selecionaForm = function () {
        var tipo = $('#id_tipo').val();

        if (tipo.toLowerCase().indexOf('valor') >= 0) {
            $('.percent').removeClass('show').addClass('hide').hide();
            $('.valor').removeClass('hide').addClass('show').show();
        } else if (tipo.toLowerCase().indexOf('percentual') >= 0) {
            $('.valor').removeClass('show').addClass('hide').hide();
            $('.percent').removeClass('hide').addClass('show').show();
        } else if (tipo.indexOf('Zerar o Frete') >= 0) {
            $('.valor').removeClass('show').addClass('hide').hide();
            $('.percent').removeClass('show').addClass('hide').hide();
        }

        if (tipo.toLowerCase().indexOf('nominal') >= 0) {
            $('.cliente').show();
        } else {
            $('.cliente').hide();
        }
    };
    var addBtn = function () {
        $('#id_codigo').parent()
            .prepend('<button class="btn" id="btn-gerar-codigo" type="button" alt="Gerar novo código" title="gerar novo código"><i class="icon-random"></i></button>')
            .addClass('input-prepend');
    };

    function makeid(tam) {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

        for (var i = 0; i < tam; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }
}(Suit.$));

