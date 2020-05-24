
$('#proyecto').on('change', ajaxDeveloper);

function ajaxDeveloper() {
    var idProyecto = $(this).val();

    $('#developer')
        .empty()
        .append('<option selected="selected" value="">Seleccione Developer</option>');


    if (idProyecto != "") {
        $.ajax({
            data: { 'idProyecto': idProyecto },
            url: "/ajax_developer/",
            type: 'get',
            success: function (data) {

                for (var i = 0; i < data.length; i++) {
                    optionText = data[i].username;
                    optionValue = data[i].id;

                    $('#developer').append(`<option value="${optionValue}"> 
                ${optionText} 
           </option>`);
                }
            }
        });
    }
}
