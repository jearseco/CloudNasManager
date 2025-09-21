// Espera a que todo el contenido de la página se cargue
document.addEventListener('DOMContentLoaded', function() {

    // Selecciona el botón por su ID
    const downloadBtn = document.getElementById('downloadBtn');

    // Añade un "escuchador" para el evento 'click'
    downloadBtn.addEventListener('click', function(event) {
        
        // 1. Previene la descarga inmediata para poder mostrar la animación
        event.preventDefault();

        // Si el botón ya está en estado de 'clic', no hagas nada más
        if (this.classList.contains('clicked')) {
            return;
        }

        // 2. Guarda la URL de descarga que está en el botón
        const downloadUrl = this.href;

        // 3. Añade la clase 'clicked' al botón para iniciar la animación CSS
        this.classList.add('clicked');

        // 4. Espera 2 segundos (2000 milisegundos) para que la animación termine
        setTimeout(function() {
            
            // 5. Inicia la descarga del archivo
            window.location.href = downloadUrl;

            // 6. (Opcional) Resetea el botón a su estado original después de otros 2 segundos
            setTimeout(function() {
                downloadBtn.classList.remove('clicked');
            }, 2000);

        }, 2000);
    });
});