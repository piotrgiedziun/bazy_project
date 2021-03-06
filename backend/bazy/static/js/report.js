$(function() {
    // arrows handler
    $(".report").click(function(e) {
        var clicked = $(this);

        $(".alert-success").hide();
        $(".modal-body, .modal-footer").show();

        $("#message").removeAttr('readonly');

        $('.date').text(clicked.attr('data-date'));
        $('.type').text(clicked.attr('data-type'));
        $('.price').text(clicked.attr('data-price'));
        $('#message').val('').focus();

        $('#reportModal').modal('show');
        e.preventDefault();
        return false;
    });

    $(".send").click(function(e) {
        var btn = $(this);
        btn.button('loading');
        $("#message").attr('readonly', true);
        setTimeout(function () {
            btn.button('reset');
            $("#message").removeAttr('readonly');
            $(".modal-body, .modal-footer").hide();
            $(".alert-success").show();
        }, 2000);
        e.preventDefault();
        return false;
    });
});