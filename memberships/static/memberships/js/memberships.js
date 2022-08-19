$(document).ready(function () {
    console.log("Before");
    

    // Gather the checkboxes
    var initial_checkboxes = document.querySelectorAll("input.form-check-input");
    // Ensure the checkboxes are gathered even when user information isn't autofilled
    if (initial_checkboxes.length <= 0) {
        var initial_checkboxes = document.querySelectorAll("input.form-check-input.is-invalid");
    }
    // Add onclick event listeners to the checkboxes
    var checkbox_divs = document.querySelectorAll("div.form-check");
    for (var i = 0; i < checkbox_divs.length; i++) {
        checkbox_divs[i].firstElementChild.addEventListener("click", checkboxTotal);
    }
    // Add onchange event listener to the select membership dropdown
    var membership_select = document.getElementById("id_membership");
    membership_select.addEventListener("change", checkMembership)
    var membership_ids = [1,2,3]
    
    var limit = 5;
    
    
    // Get this function to set all the values we need in the checkbox form
    async function getMemberships(membership_id) {
        let response = await fetch('/memberships/membership_signup', {
            method: 'get',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        let membership_data = await response.json()
        console.log(membership_data["context"]["1"]["name"])
        var membership_data_list = membership_data["context"]
        console.log(membership_data_list)
        console.log(membership_id)
        return membership_data
    }
    
    // Get the membership id from the membership field
    function checkMembership() {
        // initially check the membership selection isn't empty
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
        // Now return the id of the selected membership
        return membership_select.value;
    }
    
    
    
    // Collect the selected items in an object and count them
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
    var membership_id = checkMembership();
    console.log(membership_id);
    var membership_data = getMemberships(membership_id);
    console.log(membership_data);
    console.log("After");
})

// MEMBERSHIP DATA FROM GET MEMBERSHIPS AND SET THE ATTRIBUTES TO THEIR ACTIVITY NUMBER
// WE CAN THEN COMPARE THE ACTIVITY NUMBER WITH THE ID IN CHECK MEMBERSHIP TO SET THE LIMIT