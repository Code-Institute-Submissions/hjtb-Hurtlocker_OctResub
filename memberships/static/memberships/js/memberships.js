$(document).ready(function () {
    console.log("Before");
    
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
        var unchecked = document.querySelectorAll('input[class=form-check-input]:not(:checked)');
        console.log(unchecked);
        if (Object.keys(selections).length >= limit) {
            console.log(unchecked);
            for (var i = 0; i < unchecked.length; i++) {
                unchecked[i].setAttribute("disabled", "disabled");
            }
        }
        else {
            for (var i = 0; i < unchecked.length; i++) {
                unchecked[i].removeAttribute("disabled");
            }
        }
        console.log(selections);
        console.log("After");
    }
    checkboxTotal()
})

        // var checkbox_divs = document.getElementsByClassName("form-check");
        // console.log(checkbox_divs);
        // var limit = 5;
        // var counter = 0;
        // for (var i = 0; i < checkbox_divs.length; i++) {
        //     if (checkbox_divs[i].firstElementChild.checked) {
        //         console.log(checkbox_divs[i].outerText);
        //         counter++;
        //         if (counter >= limit) {
        //             console.log("Limit exceeded");
        //         }
        //     }
        // }

        // var selections = {};
        // var checkboxElems = document.querySelectorAll("input[type='checkbox']");
        // var totalElem = document.getElementById("seats-total");
        // var seatsElem = document.getElementById("selected-seats");

        // for (var i = 0; i < checkboxElems.length; i++) {
        //   checkboxElems[i].addEventListener("click", displayCheck);
        // }

        // function displayCheck(e) {
        //   if (e.target.checked) {
        //     selections[e.target.id] = {
        //       name: e.target.name,
        //       value: e.target.value
        //     };
        //   } 
        //   else {
        //     delete selections[e.target.id];
        //   }

        //   var result = [];
        //   var total = 0;

        //   for (var key in selections) {
        //     console.log(key);
        //   }

        //   totalElem.innerText = total;
        //   seatsElem.innerHTML = result.join("");
        // }

        // function ValidateActivitySelection() {
        //     console.log(checkboxes);
        //     var numberOfCheckedItems = 0;
        //     for (var i = 0; i < checkboxes.length; i++) {
        //         if (checkboxes[i].checked)
        //             numberOfCheckedItems++;
        //     }
        //     if (numberOfCheckedItems > 2) {
        //         alert("You can't select more than two activities!");
        //         return false;
        //     }
        // }
