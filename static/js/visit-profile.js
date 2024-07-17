function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function Name() {
    const namesubmit = document.getElementById('namesubmit');
   
    namesubmit.addEventListener('click', function(event) {
        event.preventDefault();
        
        const name = document.getElementById('name').value;

        if (!name) {
            alert('Nome Vazio');
            return;
        }
    
        if (name.length < 8) {
            alert('O nome deve ter pelo menos 8 caracteres.');
            return;
        }
        
        const formData = new FormData();
        formData.append('name', name);

        const csrfToken = getCookie('csrftoken');

        fetch('/mudar-nome/', { 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao processar a requisição');
            }
            return response.text();
        })
        .then(html => {
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    });
}

function validateAndSubmitPasswordForm(event) {
    event.preventDefault();

    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;

    if (!password || !password2) {
        alert('Por favor, preencha todos os campos de senha.');
        return;
    }

    if (password.length < 8) {
        alert('A senha deve ter pelo menos 8 caracteres.');
        return;
    }

    if (password !== password2) {
        alert('As senhas não coincidem.');
        return;
    }

    const formData = new FormData();
    formData.append('password', password);

    const csrfToken = getCookie('csrftoken');

    fetch('/mudar-senha/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao processar a requisição');
        }
        return response.text();
    })
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function handleImageSubmit(event) {
    event.preventDefault();

    const imageInput = document.getElementById('image');
    const image = imageInput.files[0];

    if (!image) {
        alert('Por favor, selecione uma imagem.');
        return;
    }

    const formData = new FormData();
    formData.append('image', image);

    const csrfToken = getCookie('csrftoken');

    fetch('/mudar-imagem/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao processar a requisição');
        }
        return response.text();
    })
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const passwordForm = document.getElementById('passwordForm');
    passwordForm.addEventListener('submit', validateAndSubmitPasswordForm);

    const imageForm = document.getElementById('imageForm');
    imageForm.addEventListener('submit', handleImageSubmit);

    Name()
});