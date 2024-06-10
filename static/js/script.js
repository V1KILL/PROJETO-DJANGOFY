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
    
})