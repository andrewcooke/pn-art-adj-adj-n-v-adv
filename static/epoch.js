
$(document).ready(function() {
    $('.epoch').each(function() {
        var epoch = $(this).text();
        if (epoch === 'None') {
            epoch = 'now';
        } else {
            date = new Date(1000 * parseInt(epoch));
            epoch = date.toLocaleString();
        }
        $(this).text(epoch);
    })
});
