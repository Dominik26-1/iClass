$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 3000);
});

function closeMessage() {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}