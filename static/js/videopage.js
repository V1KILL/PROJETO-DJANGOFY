console.log('tudo certo')
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.video').forEach(video => {
        video.addEventListener('click', function() {
            var videoId = this.dataset.id; // Obtém o ID do vídeo a partir do atributo data-id
            var csrfTokenElement = document.querySelector('input[name=csrfmiddlewaretoken]');
            
            if (csrfTokenElement) {
                var csrfToken = csrfTokenElement.value;
  
                var requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ videoId: videoId })
                };
  
                fetch('/video/', requestOptions) // Certifique-se de que este é o endpoint correto
                .then(response => {
                    if (response.ok) {
                        return response.text(); // Obtém o HTML da resposta
                    } else {
                        throw new Error('Erro ao carregar vídeo');
                    }
                })
                .then(html => {
                    console.log(html); // Logar a resposta HTML para verificação
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
