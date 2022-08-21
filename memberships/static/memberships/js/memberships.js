$(document).ready(function () {
    console.log("Before");


    // Gather the checkboxes
    var initial_checkboxes = document.querySelectorAll("input.form-check-input");
    // Ensure the checkboxes are gathered even when user information isn't autofilled
    if (initial_checkboxes.length <= 0) {
        var initial_checkboxes = document.querySelectorAll("input.form-check-input.is-invalid");
    }
    // Add onclick event listeners to the checkboxes
    const checkbox_divs = document.querySelectorAll("div.form-check");
    for (var i = 0; i < checkbox_divs.length; i++) {
        checkbox_divs[i].firstElementChild.addEventListener("click", checkboxTotal);
    }
    // Add onchange event listener to the select membership dropdown
    const membership_select = document.getElementById("id_membership");
    membership_select.addEventListener("change", checkMembership)
    
    // Get the options from the dropdown element
    const membership_options_list = membership_select.options;

    // Retrieve the membership ids for reference
    var membership_ids = []
    for (var i = 0; i < membership_options_list.length; i++) {
        if (membership_options_list[i].value > 0){
            membership_ids.push(membership_options_list[i].value)
        }
    }
    getMemberships();

    var activity_limit = checkMembership();
    console.log(activity_limit);


    
    // Get this function to set all the values we need in the checkbox form
    async function getMemberships() {
        let response = await fetch('/memberships/membership_signup', {
            method: 'get',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        let membership_data = await response.json()
        var membership_data_list = membership_data["context"]
        // var membership_activity_limits = []

        for (var i = 0; i < membership_options_list.length; i++) {
            var option_value = membership_options_list[i].attributes.value.value;
            if (option_value > 0){
                var data_activity = membership_data_list[option_value.toString()].activities;
                membership_options_list[i].setAttribute('data-activity', data_activity)
                // limit_object = {
                //     membership_id: option_value.toString(),
                //     activities: data_activity.toString(),
                // }
                // membership_activity_limits.push(limit_object);
                // membership_selection = checkMembership();
                // console.log(membership_selection);
            }
        }
        // console.log(membership_activity_limits);
        // return membership_activity_limits
    }
    


    // Get the membership id from the membership field
    function checkMembership() {
        // initially check the membership selection isn't empty
        if (!membership_ids.includes(membership_select.value)) {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].setAttribute("disabled", "disabled");
            }
        }
        else {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].removeAttribute("disabled");
            }
        }
        var activity_limit = membership_select.options[membership_select.selectedIndex].getAttribute('data-activity');
        // Now return the activity limit
        return activity_limit;
    }



    var selections = {};
    // Collect the selected checkbox items in an object and count them
    // Then disable the remaining checkboxes when we reach our limit
    function checkboxTotal() {
        var activity_limit = checkMembership();
        console.log(activity_limit)
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
        if (Object.keys(selections).length >= activity_limit) {
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

    checkboxTotal(activity_limit);
    checkMembership()
})
