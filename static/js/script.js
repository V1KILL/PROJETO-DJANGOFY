const swiper = new Swiper('.swiper', 
    // Optional parameters
    
    loop: true,
    slidesPerView: 2,
    spaceBetween: 16,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  
    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },
});

document.getElementById('btn-pagar').addEventListener('click', function() {
  // Lógica para chamar a view de processamento de pagamento via AJAX
  fetch('/pagamento')
      .then(response => response.json())
      .then(data => {
          if (data.url_pagamento) {
              // Redireciona o usuário para a página de pagamento do PagSeguro
              window.location.href = data.url_pagamento;
          } else {
              alert('Erro ao processar pagamento: ' + data.erro);
          }
      })
      .catch(error => {
          console.error('Erro ao processar pagamento:', error);
      });
});