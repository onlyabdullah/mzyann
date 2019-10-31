function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}
$(document).ready(function() {
$('.carousel').carousel({
    interval: false
});
$('.lazy-loader').Lazy();
if ($('#id_job').val()) {
    $.ajax({
        url: $('#id_job').attr('data-url'),
        data: {'job': $('#id_job').val(), 'item': getUrlVars()['item']},
        type: 'get',
        dataType: 'json',
        success: function(data) {
            if (data.is_valid) {
                is_selected = function(selected_value, value) {
                    if (selected_value == value) {
                        return "selected"
                    }
                    return null
                }
                for (let i = 0; i < data.item_options.length; i++) {
                    $('#id_item').append(
                        "<option value='" + data.item_options[i][0] + "'" + is_selected(data.selected_item, data.item_options[i][0]) + ">"+ data.item_options[i][1] +"</option>"
                    );
                }
            }
        }
    })
}
if (window.innerWidth <= 991) {
    $('#search_form_panel').addClass('is-collapse');
    $('#filter_form_panel').addClass('is-collapse');
}
});
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
let from = 0;
let to = 0;
$('#price_filter').ionRangeSlider({
type: 'double',
min: 0,
max: 10000,
step: 50,
postfix: ' E.L.',
onStart: function(data) {
    if ($('#id_price_from').val()) {
        data.from = $('#id_price_from').val();
    } else {
        data.from = 0;
    }
    if ($('#id_price_to').val()) {
        data.to = $('#id_price_to').val();
    } else {
        data.to = 10000;
    }
},
onChange: function(data) {
    $('#id_price_from').val(data.from);
    $('#id_price_to').val(data.to);
}
});
$("#filter_result_btn").on('click', function() {
const search_form_data = $('#search_form').serialize();
const filter_result_form_data = $('#filter_result_form').serialize();
url = $("#filter_result_form").attr('action') + "?" + search_form_data + "&" + filter_result_form_data;
window.location.href = url;
});