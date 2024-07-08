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
        if (!response.ok) {
          throw new ERROR('Error Then')
        }
        return response.text();
      })
      .then(html => {
        document.open();
        document.write(html);
        document.close();
      })
      .catch(error => {
        console.error('Erro', error);
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

var visit_perfil = document.getElementById('visit-perfil')
visit_perfil.addEventListener('click', function () {
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

var new_video = document.getElementById('new-video')
new_video.addEventListener('click', function () {
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

var new_topic_and_module = document.getElementById('new-topic-and-module')
new_topic_and_module.addEventListener('click', function () {
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


var stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
document.querySelector("button .checkout").addEventListener("click", function () {
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    alert("fefef")
    fetch("{% url 'create-checkout-session' %}", {
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken }
    })
    .then(response => response.json())
    .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
    .then(result => {
        if (result.error) {
            alert(result.error.message);
        }
    })
    .catch(error => console.error("Error:", error));
});
    // Create an instance of the Stripe object with your publishable API key
