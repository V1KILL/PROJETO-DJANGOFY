

document.addEventListener('DOMContentLoaded', function () {
  var splides = document.querySelectorAll('.splide');
  splides.forEach(function(splide) {
      
      new Splide(splide, {
        focus    : '0',
        autoWidth: true,
        pagination: false,
      }).mount();
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var perfil = document.querySelector('.perfil-image');
  var options = document.querySelector('.options');

  perfil.addEventListener('click', function() {
    if (options.style.display === 'flex') {
      options.style.display = 'none';
    } else {
      options.style.display = 'flex';
    }
  });
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
  var url = this.getAttribute('data-url');
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new ERROR('Error Then')
      }
      window.location.href = url;
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })
})

var createvideo = document.getElementById('createvideo')
createvideo.addEventListener('click', function () {
  var url = this.getAttribute('data-url');

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new ERROR('Error Then')
      }
      window.location.href = url;
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })
})

var createtopicandmodule = document.getElementById('createtopicandmodule')
createtopicandmodule.addEventListener('click', function () {
  var url = this.getAttribute('data-url');
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new ERROR('Error Then')
      }
      window.location.href = url;
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })
})

var logout = document.getElementById('logout')
logout.addEventListener('click', function () {
    fetch('logout')
      .then(response => {
        if (!response.ok) {
          throw new ERROR('Error Then')
        }
        window.location.href = 'login';
      })
      .catch(error => {
        console.error('erro meu amigo', error)
      })
})
