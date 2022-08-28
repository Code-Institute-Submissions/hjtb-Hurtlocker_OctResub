$(document).ready(function () {
    let submitButton = document.getElementById("signupButton");
    if (submitButton !== null) {
        submitButton.addEventListener("click", () => {
            fetch("/memberships/create_checkout_session")
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