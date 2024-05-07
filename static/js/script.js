var perfil = document.querySelector('.perfil');
var perfilOptions = document.querySelector('.perfil-options');

perfil.addEventListener("mouseenter", function() {
    setTimeout(function() {
        perfilOptions.style.display = 'flex';
    }, 100);
    perfilOptions.style.opacity = '1';
});

perfil.addEventListener("mouseleave", function() {
    setTimeout(function() {
        perfilOptions.style.display = 'none';
    }, 300);
    perfilOptions.style.opacity = '0';
});