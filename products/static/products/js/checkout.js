document.addEventListener('DOMContentLoaded', function () {
    const stripeRadio = document.getElementById('stripe');
    const codRadio = document.getElementById('cod');
    const stripeContainer = document.getElementById('stripe-card-element-container');

    function toggleStripeElement() {
      if (!stripeContainer) return; // nothing to toggle
      if (stripeRadio && stripeRadio.checked) {
        stripeContainer.style.display = 'block';
      } else {
        stripeContainer.style.display = 'none';
      }
    }

    // Attach listeners only when the elements exist (avoids "cannot read properties of null").
    if (stripeRadio) {
      stripeRadio.addEventListener('change', toggleStripeElement);
    }
    if (codRadio) {
      codRadio.addEventListener('change', toggleStripeElement);
    }

    // Run on page load to set correct initial state (safe even if elements missing)
    toggleStripeElement();
  });