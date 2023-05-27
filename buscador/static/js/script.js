    // Obtener el elemento del botón y el elemento del título
    var btnEnviar = document.getElementById('btn_enviar');
    var h1Modificar = document.getElementById('h1_modificar');

    // Agregar un controlador de eventos clic al botón
    btnEnviar.addEventListener('click', function() {
        // Cambiar el valor del título cuando se hace clic en el botón
        h1Modificar.textContent = 'clickeado';
    });