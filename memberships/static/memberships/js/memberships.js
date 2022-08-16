$(document).ready(function () {
    console.log("Before");
    
    var limit = 5;

    // async function getMemberships() {
    //     let response = await fetch('/memberships/membership_data', {
    //         method: 'get',
    //         headers: {
    //             'X-Requested-With': 'XMLHttpRequest',
    //             'Content-Type': 'application/json'
    //         }
    //     })
    //     let membership_data = await response.json()
    //     console.log(await membership_data)
    // }
    // getMemberships()

    var membership_select = document.getElementById("id_membership");
    membership_select.addEventListener("change", checkMembership)

    var initial_checkboxes = document.querySelectorAll("input[class=form-check-input]");
    var membership_ids = [1, 2, 3, 4, 5]
    function checkMembership() {
        if (!membership_ids.includes(parseInt(membership_select.value))) {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].removeAttribute("checked");
                initial_checkboxes[i].setAttribute("disabled", "disabled");
                console.log(initial_checkboxes[i]);
            }
        }
        else {
            for (var i = 0; i < initial_checkboxes.length; i++) {
                initial_checkboxes[i].removeAttribute("disabled");
            }
        }
    }


    console.log(initial_checkboxes);
    

    // Add onclick event listeners to the checkboxes
    var checkbox_divs = document.querySelectorAll("div.form-check");
    for (var i = 0; i < checkbox_divs.length; i++) {
        checkbox_divs[i].firstElementChild.addEventListener("click", checkboxTotal);
        checkbox_divs[i].firstElementChild.name = checkbox_divs[i].outerText;
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

        // deactivate the remaining unchecked boxes when we have selecte the limit
        var remaining_unchecked = document.querySelectorAll("input[class=form-check-input]:not(:checked)");
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
        console.log("After");
    }
    checkboxTotal()
    checkMembership()
})