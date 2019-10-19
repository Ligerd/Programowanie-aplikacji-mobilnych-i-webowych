

document.addEventListener('DOMContentLoaded', function () {
    const lastname = document.getElementById("lastname");
    lastname.addEventListener("input", myFunction);

    function myFunction() {
        console.log(lastname.value)
    }

});