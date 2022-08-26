$(document).ready(function () {
    var stripe_public_key = document.getElementById('stripe_public_key').innerText.slice(1, -1);
    var client_secret = document.getElementById('client_secret').innerText.slice(1, -1);
    console.log(stripe_public_key);
    console.log(client_secret);
    var stripe = Stripe(stripe_public_key);
    var elements = stripe.elements();
    var style = {
        base: {
            color: 'rgb(255,255,255)',
            iconColor: 'rgb(255,255,255)',
            fontFamily: '"Roboto Condensed", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '20px',
            '::placeholder': {
                color: 'rgba(255,255,255, 0.5)'
            }
        },
        invalid: {
            color: 'rgb(187, 0, 0)',
            iconColor: 'rgb(187, 0, 0)'
        }
    };
    var card = elements.create('card', {style: style});
    card.mount('#payment-details');
})
