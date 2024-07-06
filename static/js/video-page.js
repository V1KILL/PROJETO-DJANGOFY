var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
var likeButton = document.querySelector('.buttons a.like');
var checkButton = document.querySelector('.buttons a.check');

function postRequest(url, data) {
    var requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    };

    return fetch(url, requestOptions)
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

function Video() {
    document.querySelectorAll('.video').forEach(video => {
        video.addEventListener('click', function() {
            var videoId = this.dataset.id;
            var moduleId = likeButton.getAttribute("data-moduleid");
            var topicId = likeButton.getAttribute("data-topicid");

            postRequest('/video/', { videoId: videoId, moduleId: moduleId, topicId: topicId });
        });
    });
}

function Like() {
    
    likeButton.addEventListener('click', function() {

        var moduleId = likeButton.getAttribute("data-moduleid");
        var videoId = likeButton.getAttribute("data-videoid");
        var topicId = likeButton.getAttribute("data-topicid");

        postRequest('/like/', { moduleId: moduleId, videoId: videoId, topicId: topicId });
    });
    
}

function Check() {
    
    checkButton.addEventListener('click', function() {
        var moduleId = checkButton.getAttribute("data-moduleid");
        var videoId = checkButton.getAttribute("data-videoid");
        var topicId = checkButton.getAttribute("data-topicid");

        postRequest('/check/', { moduleId: moduleId, videoId: videoId, topicId: topicId });
    });
    
}

function Comment() {
    var commentButton = document.querySelector('.comentar button');
    commentButton.addEventListener('click', function() {
        var moduleId = checkButton.getAttribute("data-moduleid");
        var videoId = checkButton.getAttribute("data-videoid");
        var topicId = checkButton.getAttribute("data-topicid");
        var comentario = document.querySelector('.comentar input').value;

        if (comentario) {
            var dados = { comentario: comentario, moduleId: moduleId, videoId: videoId, topicId: topicId };
            postRequest('/comment/', dados);
        }
    });
}

function Reply() {
    document.querySelectorAll('.subcomentariodescricao button').forEach(button => {
        button.addEventListener('click', function() {
            var moduleId = checkButton.getAttribute("data-moduleid");
            var videoId = checkButton.getAttribute("data-videoid");
            var topicId = checkButton.getAttribute("data-topicid");
            var comentarioId = this.dataset.id;
            var comentario = this.previousElementSibling.value;

            if (comentario) {
                var dados = { comentario: comentario, moduleId: moduleId, videoId: videoId, topicId: topicId, comentarioId: comentarioId };
                postRequest('/reply/', dados);
            }
        });
    });
}

function VideoEditPage() {

    editbutton = document.querySelector('.video-edit-page')
    
    editbutton.addEventListener('click', function() {
        
        var moduleId = likeButton.getAttribute("data-moduleid");
        var videoId = likeButton.getAttribute("data-videoid");
        var topicId = likeButton.getAttribute("data-topicid");

        postRequest('/video-edit-page/', { moduleId: moduleId, videoId: videoId, topicId: topicId });
    });
}



document.addEventListener('DOMContentLoaded', function() {
    Video();
    Like();
    Check();
    Comment();
    Reply();
    VideoEditPage();
    
});
