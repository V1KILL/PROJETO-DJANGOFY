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
    var valuemodule = this.id
    var url = this.dataset.url

    if (valuemodule == 'stripebutton') {
      var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
      var stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");

      fetch(url, {
        method: "POST",
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      .then(function (response) {
        return response.json();
      })
      .then(function (session) {
        return stripe.redirectToCheckout({ sessionId: session.id });
      })
      .then(function (result) {
        // If redirectToCheckout fails due to a browser or network
        // error, you should display the localized error message to your
        // customer using error.message.
        if (result.error) {
          alert(result.error.message);
        }
      })
      .catch(function (error) {
        console.error("Error:", error);
      });

    } else {
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
          throw new Error('Error Then');
        }
        return response.text();
      })
      .then(html => {
        document.open();
        document.write(html);
        document.close();
      })
      .catch(error => {
        console.error('Error', error);
      });
    }
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
    // Create an instance of the Stripe object with your publishable API key
