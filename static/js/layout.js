$(document).ready(function () {
    $(".floating-notification").fadeIn().delay(2000).fadeOut();
});

document.addEventListener('DOMContentLoaded', function () {
    const enableEditButton = document.getElementById('enable_edit_button');
    if (enableEditButton) {
        enableEditButton.addEventListener('click', function () {
            const form = document.getElementById('edit_form');
            if (form) {
                const inputs = form.getElementsByTagName('input');
                const selects = form.getElementsByTagName('select');
                const editButton = document.getElementById('edit_button');

                for (const input of inputs) {
                    if (input.type !== 'hidden') {
                        input.disabled = !input.disabled;
                    }
                }

                for (const select of selects) {
                    select.disabled = !select.disabled;
                }

                if (editButton) {
                    editButton.classList.toggle('edit-button');
                    editButton.classList.toggle('edit-button-visible');
                }
            }
        });
    }

    const svgInput = document.getElementById('svg_recinto');
    if (svgInput) {
        svgInput.addEventListener('change', mostrarPrevisualizacion);
    }
});

function mostrarPrevisualizacion() {
    const input = document.getElementById('svg_recinto');
    const previewContainer = document.getElementById('preview-container');

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const previewObject = document.createElement('object');
            previewObject.type = 'image/svg+xml';
            previewObject.data = e.target.result;
            previewObject.style.width = '100%';
            previewObject.style.height = '100%';
            previewContainer.innerHTML = '';
            previewContainer.appendChild(previewObject);
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        previewContainer.innerHTML = '';
    }
}

function mostrarPrevisualizacion() {
    var input = document.getElementById('svg_recinto');
    var previewContainer = document.getElementById('preview-container');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var previewImage = document.createElement('img');
            previewImage.src = e.target.result;
            previewContainer.innerHTML = '';
            previewContainer.appendChild(previewImage);
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        previewContainer.innerHTML = '';
    }
}

const downloadBtn = document.getElementById('downloadBtn');
if (downloadBtn) {
    downloadBtn.addEventListener('click', function () {
        const svgElement = document.querySelector('.s-details-container-right svg');
        if(svgElement) {
            const svgContent = svgElement.outerHTML;
            const blob = new Blob([svgContent], { type: 'image/svg+xml' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'tu_archivo.svg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert("No se encontró ningún SVG para descargar.");
        }
    });
}

document.getElementById('openModalBtn').addEventListener('click', openModal);

function openModal() {
    document.getElementById('myModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Cierra el modal si se hace clic fuera de él
window.addEventListener('click', function (event) {
    var modal = document.getElementById('myModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});


const checkbox = document.getElementById('edit_status');
const hiddenField = document.getElementById('edit_status_hidden');

checkbox.addEventListener('change', () => {
    hiddenField.value = checkbox.checked ? 'true' : '';
});

const checkboxAxis = document.getElementById('edit_axis');
const hiddenFieldAxis = document.getElementById('edit_axis_hidden');

checkboxAxis.addEventListener('change', () => {
    hiddenFieldAxis.value = checkboxAxis.checked ? 'true' : '';
});


const checkboxAlignment = document.getElementById('edit_alignment');
const hiddenFieldAlignment = document.getElementById('edit_alignment_hidden');

checkboxAlignment.addEventListener('change', () => {
    hiddenFieldAlignment.value = checkboxAlignment.checked ? 'true' : '';
});

function toggleFieldset() {
    var fieldsetContent = document.getElementById('fieldsetContent');
    if (fieldsetContent.style.display === 'none') {
        fieldsetContent.style.display = 'block';
    } else {
        fieldsetContent.style.display = 'none';
    }
}

function toggleAnotherFieldset() {
    var anotherFieldsetContent = document.getElementById('anotherFieldsetContent');
    if (anotherFieldsetContent.style.display === 'none') {
        anotherFieldsetContent.style.display = 'block';
    } else {
        anotherFieldsetContent.style.display = 'none';
    }
}

function toggleDropdown(event) {
    const target = event.target;
    const dropdownContent = target.closest('.dropdown').querySelector('.dropdown-content');

    // Verifica si el evento proviene del botón o el icono
    const isButton = target.classList.contains('config-button');
    const isIcon = target.id === 'gear_icon';

    // Si el evento proviene del botón o el icono, alternamos la clase 'show' en el menú desplegable
    if (isButton || isIcon) {
        const allDropdowns = document.querySelectorAll('.dropdown-content');
        allDropdowns.forEach(dropdown => {
            // Si el menú desplegable no es el mismo que el menú desplegable actual, lo cerramos
            if (dropdown !== dropdownContent) {
                dropdown.classList.remove('show');
            }
        });
        // Alternamos el menú desplegable actual
        dropdownContent.classList.toggle('show');
    } else {
        // Si el evento no proviene del botón o el icono, cerramos todos los menús desplegables
        const dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(dropdown => dropdown.classList.remove('show'));
    }
}

// Cierra el menú si el usuario hace clic fuera de él
window.onclick = function (event) {
    if (!event.target.matches('.config-button')) {
        const allDropdowns = document.querySelectorAll('.dropdown-content');
        allDropdowns.forEach(dropdownItem => {
            if (dropdownItem.classList.contains('show')) {
                dropdownItem.classList.remove('show');
            }
        });
    }
}
