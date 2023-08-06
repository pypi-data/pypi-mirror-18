$(document).ready(function() {
    // add the link delete the box
    $('.cbox-content').prepend('<p id="delete-box"><a href="#">delete box</a></p>');

    // add event to delete the box
    $('#delete-box a').click(function() {
        $('.cbox').remove();
        return false;
    });

});
