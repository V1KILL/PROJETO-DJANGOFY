document.addEventListener('DOMContentLoaded', function () {
    new Splide('.splide', {
        type   : 'loop',
        perPage: 3,
        autoplay: true,
    }).mount();
});

var likeButton = document.querySelector('.buttons a.like');
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.video').forEach(video => {
        video.addEventListener('click', function() {
            var videoId = this.dataset.id;
            
            var moduleId = likeButton.getAttribute("data-moduleid");
            
            var topicId = likeButton.getAttribute("data-topicid");
            var csrfTokenElement = document.querySelector('input[name=csrfmiddlewaretoken]');
            
            if (csrfTokenElement) {
                var csrfToken = csrfTokenElement.value;
  
                var requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ videoId: videoId, moduleId: moduleId, topicId:topicId })
                };
  
                fetch('/video/', requestOptions)
                .then(response => {
                    if (response.ok) {
                        return response.text();
                    } else {
                        throw new Error('Erro ao carregar vídeo');
                    }
                })
                .then(html => {
                    console.log(html);
                    document.open();
                    document.write(html);
                    document.close();
                })
                .catch(error => {
                    console.error('Erro ao carregar vídeo', error);
                });
            } else {
                console.error('Token CSRF não encontrado');
            }
        });
    });
});

var logo = document.getElementById('logo')
logo.addEventListener('click', function () {

  fetch('/')
    .then(response => {
      if (!response.ok) {
        throw new ERROR('Error Then')
      }
      window.location.href = '/';
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })

})

var perfil = document.querySelector('.perfil');
var options = document.querySelector('.perfil-image .options');

perfil.addEventListener('click', function() {

  if (options.style.display === 'flex') {
    options.style.display = 'none';
  } else {
    options.style.display = 'flex';
  }
});

document.addEventListener('DOMContentLoaded', function() {
    var likeButton = document.querySelector('.buttons a.like');
    if (likeButton) {
        likeButton.addEventListener('click', function(event) {
          event.preventDefault();

        var moduleId = likeButton.getAttribute("data-moduleid");
        var videoId = likeButton.getAttribute("data-videoid");
        var topicId = likeButton.getAttribute("data-topicid");
        var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        var requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ moduleId: moduleId, videoId: videoId, topicId: topicId })
        };

        fetch('/like/', requestOptions) 
          .then(response => {
              if (response.ok) {
                  return response.text(); 
              } else {
                  throw new Error('Erro ao carregar vídeo');
              }
          })
          .then(html => {
              console.log(html); // L
              document.open();
              document.write(html);
              document.close();
          })
          .catch(error => {
              console.error('Erro ao carregar vídeo', error);
          });
      });
  }
});

document.addEventListener('DOMContentLoaded', function() {
    var checkButton = document.querySelector('.buttons a.check');
    if (checkButton) {
        checkButton.addEventListener('click', function(event) {
          event.preventDefault();

        var moduleId = checkButton.getAttribute("data-moduleid");
        var videoId = checkButton.getAttribute("data-videoid");
        var topicId = checkButton.getAttribute("data-topicid");
        var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        var requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ moduleId: moduleId, videoId: videoId, topicId: topicId })
        };

        fetch('/check/', requestOptions) 
          .then(response => {
              if (response.ok) {
                  return response.text(); 
              } else {
                  throw new Error('Erro ao carregar vídeo');
              }
          })
          .then(html => {
              console.log(html); // L
              document.open();
              document.write(html);
              document.close();
          })
          .catch(error => {
              console.error('Erro ao carregar vídeo', error);
          });
      });
  }
});
var checkButton = document.querySelector('.buttons a.check');
document.querySelector('.comentar button').addEventListener('click', function() {
    
    var moduleId = checkButton.getAttribute("data-moduleid");
    var videoId = checkButton.getAttribute("data-videoid");
    var topicId = checkButton.getAttribute("data-topicid");
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    var comentario = document.querySelector('.comentar input').value;
    if (comentario) {
        var dados = {
            comentario: comentario,
            moduleId: moduleId,
            videoId: videoId,
            topicId: topicId
        };
   
    console.log(comentario)

    var requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(dados)
    };
    fetch('/comentar/', requestOptions) 
        .then(response => {
            if (response.ok) {
                return response.text(); 
            } else {
                throw new Error('Erro ao carregar vídeo');
            }
        })
        .then(html => {
            console.log(html); // L
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => {
            console.error('Erro ao carregar vídeo', error);
        });
    }
});


document.addEventListener('DOMContentLoaded', function() {
   
    document.querySelectorAll('.subcomentariodescricao button').forEach(function(button) {
        button.addEventListener('click', function() {
            var checkButton = document.querySelector('.buttons a.check');
            var moduleId = checkButton.getAttribute("data-moduleid");
            var videoId = checkButton.getAttribute("data-videoid");
            var topicId = checkButton.getAttribute("data-topicid");
            var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
            var comentarioId = this.dataset.id;
            var comentario = this.previousElementSibling.value;

            if (comentario) {
                var dados = {
                    comentario: comentario,
                    moduleId: moduleId,
                    videoId: videoId,
                    topicId: topicId,
                    comentarioId: comentarioId
                };

                
                var requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(dados)
                };
                fetch('/responder/', requestOptions)
                    .then(response => {
                        if (response.ok) {
                            return response.text();
                        } else {
                            throw new Error('Erro ao carregar vídeo');
                        }
                    })
                    .then(html => {
                        console.log(html);
                        document.open();
                        document.write(html);
                        document.close();
                    })
                    .catch(error => {
                        console.error('Erro ao carregar vídeo', error);
                    });
            }
        });
    });
});

