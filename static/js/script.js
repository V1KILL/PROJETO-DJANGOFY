var perfil = document.querySelector('.perfil');
var options = document.querySelector('.perfil-image .options');

perfil.addEventListener('click', function() {

  if (options.style.display === 'flex') {
    options.style.display = 'none';
  } else {
    options.style.display = 'flex';
  }
});
var module = document.querySelector('.module')
module.addEventListener('click', function(){
  var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
  var moduleId = module.getAttribute('data-id');
  console.log('estou recbend', moduleId)
  
  var requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({moduleId: moduleId})
  }
  fetch('/module', requestOptions)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error Then')
      }
      
    })
    .catch(error => {
      console.error('erro meu amigo', error)
    })
})

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