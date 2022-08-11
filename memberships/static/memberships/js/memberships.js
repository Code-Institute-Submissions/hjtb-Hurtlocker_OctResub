$(document).ready(function () {
    console.log("Before");
    var checkboxes = document.getElementsByClassName("form-check-input");
    console.log(checkboxes);
    console.log("After");

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
})
