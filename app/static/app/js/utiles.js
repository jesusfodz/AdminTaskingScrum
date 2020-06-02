function gestionTiempo() {
    var tiempoT = $('#tiempoTrabajado').val();
    var tiempoE = $('#tiempoEstimado').val();

    if tiempoT > tiempoE{
        alert();
    } else {
        tiempoR = tiempoE - tiempoT;
        $('#tiempoRestante').val(tiempoR);
    }
}

function showEliminarTareaModal(valor) {
    $('#idTareaEliminar').val(valor);
    $('#eliminarTareaModal').modal('show')
}

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

$('#developer').on('focus', ajaxDeveloper2);

function ajaxDeveloper2() {
    var idProyecto = $('#proyecto').val();

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