document.addEventListener('DOMContentLoaded', function () {
    // Inicialização do carousel
    const carousel = new bootstrap.Carousel('#heroCarousel', {
        interval: 5000, // Intervalo entre transições (5 segundos)
        ride: 'carousel'
    });

    // Function to handle the active state of nav links
    const list = document.querySelectorAll('.list');
    list.forEach((item) => item.addEventListener('click', () => {
        list.forEach((el) => el.classList.remove('active'));
        item.classList.add('active');
    }));

    // Form handling for Questionnaire
    const questionnaireForm = document.querySelector('.questionnaire-form');
    if (questionnaireForm) {
        const energyLevel = document.getElementById('energy_level');
        const energyValue = document.createElement('span');
        energyLevel.parentNode.appendChild(energyValue);
        
        energyLevel.addEventListener('input', function () {
            energyValue.textContent = this.value;
        });
        
        energyValue.textContent = energyLevel.value;
    }

    // Playlist interactions
    const playlistCards = document.querySelectorAll('.playlist-card');
    playlistCards.forEach(card => {
        card.addEventListener('click', function (e) {
            if (!e.target.classList.contains('btn-primary') && 
                !e.target.classList.contains('btn-secondary')) {
                const id = this.dataset.playlistId;
                window.location.href = `/playlist/${id}/`;
            }
        });
    });

    // Image preview for profile upload
    const imageInput = document.getElementById('profile-image-input');
    const imagePreview = document.getElementById('profile-image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Form validation for the questionnaire
    if (questionnaireForm) {
        questionnaireForm.addEventListener('submit', function (e) {
            const inputs = questionnaireForm.querySelectorAll('select');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos.');
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Image error handling for carousel
    document.querySelectorAll('.carousel-item img').forEach(img => {
        img.onerror = function () {
            this.style.display = 'none';
            this.closest('.carousel-item').style.backgroundColor = '#000';
        };
    });
});
