import 'bootstrap';
import '../scss/app.scss';

var $ = require("jquery");
let mouseDown = false;
let char_tag_mapping = new Map();
let tag_id_mapping = new Map();
let unknown_tag = '';

function load_sentences() {
    $.get(
        "api/sentence/gets",
        {},
        function( data ) {
            unknown_tag = data.unknown_tag;
            initialize_available_tags(data.available_tags);
            let result = '';
            let current_type = '';
            let current_type_displ = '';
            let current_id = 0;
            $.each(data.sentences, function (i, sentence) {
                result += `<div data-id="${i}" class="sentence col-lg-12 border border-success">`;
                $.each(sentence, function(k, word) {
                    current_type = data.tags[i][k];
                    current_id = tag_id_mapping.get(current_type);
                    current_type_displ = current_type;
                    if (current_type === unknown_tag) {
                        current_type_displ = '';
                    }
                    result += `<span class="word">${word}<span data-type="${current_id}" class="tag badge badge-info">${current_type_displ}</span></span>`
                });
                result += `</div>`;
            });
            $('#available_sentences').html(result);
        }
    );
}

function initialize_available_tags(available_tags) {
    let result = '';
    let key = '';
    $.each(available_tags, function (i, tag) {
        char_tag_mapping.set(97 + i, tag);
        tag_id_mapping.set(tag, i);
        key = String.fromCharCode(97 + i);
        result += `<div class="col-lg-4"><p>${tag} <kbd>${key}</kbd></p></div>`;
    });
    $('#available_tags').html(result);
}

function listen_to_keyboard() {
    $(document).on('keypress', function (e) {
        if (char_tag_mapping.has(e.which)) {
            let tag = char_tag_mapping.get(e.which);
            let id = tag_id_mapping.get(tag);
            if (tag === unknown_tag) {
                tag = '';
            }

            $(this).find('.word.bg-warning').find('.tag')
                .html(tag)
                .attr('data-type', id);
        }
    });
}

function bind_mouse_actions() {
    // Track mouse state and unmark on right click.
    $(document).mousedown(function() {
        mouseDown = true;
    })
    .mouseup(function() {
        mouseDown = false;
    })
    .contextmenu(function () {
        $(this).find('.word').toggleClass('bg-warning', false);
        return false;
    });

    // Toggle word markings while mouse is down.
    $('#available_sentences')
    .on('mouseover', '.word', function (e) {
        if (mouseDown) {
            if (!$(e.target).hasClass('badge')) {
                $(this).toggleClass('bg-warning');
            }
        }
    })
    .on('mousedown', '.word', function (e) {
        $(this).toggleClass('bg-warning');
    });
}


function bind_store_button() {
    $('#store-changes').click(function () {
        let tags = [];
        $('.sentence').each(function () {
            let id = $(this).attr('data-id');
            let tag = [];
            $(this).find('.tag').each(function (i, e) {
                tag.push($(this).attr('data-type'))
            });
            tags.push(tag)
        });
        console.log(tags);
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "api/sentence/update",
            data: JSON.stringify({tags: tags}),
            success: function (data) {
                alert('Stored');
            },
            dataType: "json"
        });
    });
}

$(document).ready(function() {
    load_sentences();
    listen_to_keyboard();
    bind_mouse_actions();
    bind_store_button();
});