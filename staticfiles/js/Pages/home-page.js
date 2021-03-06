$('#id_job').on('change', function() {
    item_input = $('#id_item');
    item_input.children().slice(1,).remove();
    $.ajax({
        url: $(this).attr('data-url'),
        data: {'job': $(this).val()},
        type: 'get',
        dataType: 'json',
        success: function(data) {
            if (data.is_valid) {
                for (let i = 0; i < data.item_options.length; i++) {
                    item_input.append(
                        "<option value='"+ data.item_options[i][0] +"'>"+ data.item_options[i][1] +"</option>"
                    )
                }
            }
        }
    })
});
$(document).ready(function() {
    $('body').addClass('home-page layout-full')
});