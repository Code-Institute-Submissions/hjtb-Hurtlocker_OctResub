$(document).ready(function () {
    console.log("Before");
    
    var limit = 5;

    async function getMemberships() {
        let response = await fetch('/memberships/membership_signup', {
            method: 'get',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        let membership_data = await response.json()
        return membership_data
    }
    

    var membership_select = document.getElementById("id_membership");
    membership_select.addEventListener("change", checkMembership)

    // Gather the checkboxes to disable the
    var initial_checkboxes = document.querySelectorAll("input.form-check-input");
    // Ensure the checkboxes are gathered even when user information isn't autofilled
    if (initial_checkboxes.length <= 0) {
        var initial_checkboxes = document.querySelectorAll("input.form-check-input.is-invalid");
    }
    console.log(initial_checkboxes);
    
    var membership_ids = [1,2,3,4,5]
    function checkMembership() {
        if (!membership_ids.includes(parseInt(membership_select.value))) {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].setAttribute("disabled", "disabled");
            }
        }
        else {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].removeAttribute("disabled");
            }
        }
    }
    

    // Add onclick event listeners to the checkboxes
    var checkbox_divs = document.querySelectorAll("div.form-check");
    for (var i = 0; i < checkbox_divs.length; i++) {
        checkbox_divs[i].firstElementChild.addEventListener("click", checkboxTotal);
    }

    // collect the selected items in an object and count them
    var selections = {};
    function checkboxTotal() {
        for (var i = 0; i < checkbox_divs.length; i++) {
            var checkbox = checkbox_divs[i].firstElementChild;
            if (checkbox.checked) {
                selections[checkbox.id] = {
                    name: checkbox.name,
                    value: checkbox.value
                };
            }
            else {
                delete selections[checkbox.id];
            }
        }

        // deactivate the remaining unchecked boxes when we have hit the limit
        var remaining_unchecked = document.querySelectorAll("input[class='form-check-input']:not(:checked)");
        // Ensure the checkboxes are gathered even when user information isn't autofilled
        if (remaining_unchecked.length <= 0) {
            var remaining_unchecked = document.querySelectorAll("input[class='form-check-input is-invalid']:not(:checked)");
        }
        console.log(remaining_unchecked)
        if (Object.keys(selections).length >= limit) {
            for (var i = 0; i < remaining_unchecked.length; i++) {
                remaining_unchecked[i].setAttribute("disabled", "disabled");
            }
        }
        else {
            for (var i = 0; i < remaining_unchecked.length; i++) {
                remaining_unchecked[i].removeAttribute("disabled");
            }
        }
    }
    checkboxTotal();
    checkMembership();
    var membership_data = getMemberships();
    console.log(membership_data);
    console.log("After");
})