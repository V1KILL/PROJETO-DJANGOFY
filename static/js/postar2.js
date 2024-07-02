document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#myForm');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        if (form.checkValidity()) {
            
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
            var requestOptions = {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData,
            };

            fetch('/createvideo/', requestOptions)
                .then(response => {
                    if (response.ok) {
                        return response.text();
                    } else {
                        throw new Error('Erro ao carregar módulo');
                    }
                })
                .then(data => {
                    console.log(data);
                   
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error('erro meu amigo', error);
                });
        } else {
            console.log('Formulário inválido.');
        }
    });
});
