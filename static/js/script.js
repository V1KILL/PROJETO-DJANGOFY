var perfil = document.querySelector('.perfil');
var options = document.querySelector('.perfil-image .options');

perfil.addEventListener('click', function() {

  if (options.style.display === 'flex') {
    options.style.display = 'none';
  } else {
    options.style.display = 'flex';
  }
});

document.querySelectorAll('.module').forEach(module => {
  module.addEventListener('click', function() {
    
    var moduleId = this.dataset.id;
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    var requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ moduleId: moduleId })
    };

    fetch('/module/', requestOptions) 
      .then(response => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error('Erro ao carregar módulo');
        }
      })
      .then(html => {
        console.log(html);
        document.open();
        document.write(html);
        document.close();
      })
      .catch(error => {
        console.error('erro meu amigo', error);
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

var perfil = document.getElementById('perfil')
perfil.addEventListener('click', function () {

  fetch('perfil')
    .then(response => {
      if (!response.ok) {
        throw new ERROR('Error Then')
      }
      window.location.href = 'perfil';
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })

})
