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
    var card = elements.create('card', { style: style });
    card.mount('#payment-details');
    function showCardError(event) {
        let showErrorDiv = document.getElementById('card-input-errors');
        if (event.error) {
            showErrorDiv.textContent = event.error.message;
        } else {
            showErrorDiv.textContent = '';
        }
    }
    card.addEventListener('change', function (event) {
        showCardError(event);
    });
    let submitButton = document.querySelector("#signupButton");
    if (submitButton !== null) {
        submitButton.addEventListener("click", () => {
            fetch("/memberships/checkout", {
                method: 'get',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            })
                .then((result) => { return result.json(); })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                })
                .then((res) => {
                    console.log(res);
                });
        });
    };
})