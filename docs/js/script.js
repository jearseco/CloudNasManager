document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA DEL CARRUSEL ---
    const track = document.querySelector('.carousel-track');
    if (track) {
        const slides = Array.from(track.children);
        const nextButton = document.querySelector('.carousel-button.next');
        const prevButton = document.querySelector('.carousel-button.prev');
        const slideWidth = slides[0].getBoundingClientRect().width;
        let currentIndex = 0;

        // Organiza los slides uno al lado del otro
        const setSlidePosition = (slide, index) => {
            slide.style.left = slideWidth * index + 'px';
        };
        // slides.forEach(setSlidePosition); // No es necesario con Flexbox

        const moveToSlide = (track, currentSlide, targetSlide) => {
            track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
            currentSlide.classList.remove('current-slide');
            targetSlide.classList.add('current-slide');
        };

        const updateSlide = (newIndex) => {
            const currentSlide = slides[currentIndex];
            const targetSlide = slides[newIndex];
            track.style.transform = `translateX(-${100 * newIndex}%)`;
            currentIndex = newIndex;
        };

        // Click en botón de siguiente
        nextButton.addEventListener('click', e => {
            let newIndex = currentIndex + 1;
            if (newIndex >= slides.length) newIndex = 0; // Vuelve al inicio
            updateSlide(newIndex);
        });

        // Click en botón de anterior
        prevButton.addEventListener('click', e => {
            let newIndex = currentIndex - 1;
            if (newIndex < 0) newIndex = slides.length - 1; // Va al final
            updateSlide(newIndex);
        });
    }

    // --- LÓGICA DEL BOTÓN DE DESCARGA ---
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(event) {
            event.preventDefault();
            if (this.classList.contains('clicked')) return;
            const downloadUrl = this.href;
            this.classList.add('clicked');
            setTimeout(() => {
                window.location.href = downloadUrl;
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 2000);
            }, 2000);
        });
    }
});