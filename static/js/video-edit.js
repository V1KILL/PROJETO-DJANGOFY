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

function Edit() {
    const editButtonConfirm = document.getElementById('editbuttonconfirm');

    editButtonConfirm.addEventListener('click', function(event) {
        event.preventDefault();
        
        const moduleId = document.querySelector('section a.like').getAttribute("data-moduleid");
        const videoId = document.querySelector('section a.like').getAttribute("data-videoid");
        const topicId = document.querySelector('section a.like').getAttribute("data-topicid");
        
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const url = document.getElementById('url').value;
        const capa = document.getElementById('capa').files[0]; // Corrigido para pegar o arquivo
        
        const formData = new FormData();
        formData.append('moduleId', moduleId);
        formData.append('videoId', videoId);
        formData.append('topicId', topicId);
        formData.append('title', title);
        formData.append('description', description);
        formData.append('url', url);
        if (capa) {
            formData.append('capa', capa);
        }

        const csrfToken = getCookie('csrftoken');

        var requestOptions = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        };
    
        fetch('/edit/', requestOptions)
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

document.addEventListener('DOMContentLoaded', function() {
    Edit();
});