 const stripe = Stripe('your_publishable_key_here');
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    
    const stripeContainer = document.getElementById('stripe-card-element-container');
    document.querySelectorAll('input[name="payment_method"]').forEach((elem) => {
        elem.addEventListener("change", function(event) {
            if (event.target.value === "Stripe") {
                stripeContainer.style.display = "block";
            } else {
                stripeContainer.style.display = "none";
            }
        });
    });