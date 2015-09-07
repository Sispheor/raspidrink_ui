// hide messages after a delay
setTimeout(function() {
    $('#messages').fadeOut('fast');
}, 3000); // <-- time in milliseconds

//
function open_modal_detail(id){
    var modal_id = "modal-detail-cocktail-"+id
    $('#'+modal_id).modal('show');
}

// callback function for ajax call
function ajax_callback(data){
    // Set the message content
    $('#message_content').text(data.status);
    // show the box
    var messages_callback = document.getElementById ( "messages_callback" ) ;
    messages_callback.style.visibility = "visible" ;
    jQuery("#messages_callback").fadeIn('fast');
    // hide after 3 secondes
    setTimeout(function() {
        jQuery("#messages_callback").fadeOut('fast');
    }, 3000);
}

$(document).ready(function () {
    // Code adapted from http://djangosnippets.org/snippets/1389/
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.item').remove();
            var forms = $('.item'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            var i = 0;
            // Go through the forms and set their indices, names and IDs
            for (formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).children().children().each(function () {
                    if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert("Il faut au moins une bouteille. You fucking know it.");
        }
        return false;
    }

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 16 todo items
        if (formCount < 16) {
            // Clone a form (without event handlers) from the first form
            var row = $(".item:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");

            // Relabel or rename all the relevant bits
            $(row).children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the delete item/form link
            $(row).find(".delete").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);

        } // End if
        else {
            alert("Pas plus de 15 bouteilles");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "form");
    });

    $(".delete").click(function () {
        return deleteForm(this, "form");
    });
});



