$(document).ready(function () {
    console.log("Before");

    // fetch('http://some_url.com')
    //     .then(response => response.json()) // converts the response to JSON
    //     .then(data => {
    //         console.log(data);
    //         // do something (like update the DOM with the data)
    //     });

    // var membership_select = document.getElementById("id_membership");
    // console.log(membership_select);
    // var initial_unchecked_boxes = document.querySelectorAll('input[class=form-check-input]:not(:checked)');

    // if (membership_select = "gold" || "silver" || "platinum") {
    //     for (var i = 0; i < initial_unchecked_boxes.length; i++) {
    //         initial_unchecked_boxes[i].setAttribute("disabled", "disabled");
    //     }
    // }
    // else {
    //     for (var i = 0; i < initial_unchecked_boxes.length; i++) {
    //         initial_unchecked_boxes[i].removeAttribute("disabled");
    //     }
    // }

    var checkbox_divs = document.querySelectorAll("div.form-check");
    console.log(checkbox_divs);
    for (var i = 0; i < checkbox_divs.length; i++) {
        checkbox_divs[i].firstElementChild.addEventListener("click", checkboxTotal);
        checkbox_divs[i].firstElementChild.name = checkbox_divs[i].outerText;
        console.log(checkbox_divs[i].firstElementChild);
    }

    var selections = {};
    var limit = 5;
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
        var remaining_unchecked = document.querySelectorAll('input[class=form-check-input]:not(:checked)');
        console.log(remaining_unchecked);
        if (Object.keys(selections).length >= limit) {
            console.log(remaining_unchecked);
            for (var i = 0; i < remaining_unchecked.length; i++) {
                remaining_unchecked[i].setAttribute("disabled", "disabled");
            }
        }
        else {
            for (var i = 0; i < remaining_unchecked.length; i++) {
                remaining_unchecked[i].removeAttribute("disabled");
            }
        }
        console.log(selections);
        console.log("After");
    }
    checkboxTotal()
})