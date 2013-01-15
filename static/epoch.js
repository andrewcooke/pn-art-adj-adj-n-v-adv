
$(document).ready(function() {
    $('.epoch').each(function() {
        var epoch = $(this).text();
        if (epoch === 'None') {
            epoch = 'unknown';
        } else {
            date = new Date(1000 * parseInt(epoch));
            epoch = date.toLocaleString();
        }
        $(this).text(epoch);
    })
});
