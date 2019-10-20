document.addEventListener('DOMContentLoaded', function () {
    const lastname = document.getElementById("lastname");
    lastname.addEventListener("input", functionforlastname);

    function functionforlastname(e) {
        if (e.target.value.length<5){
            document.getElementById('lastname').style.borderColor='#e52213';
            // alert("problem w name")
        }else {
            document.getElementById('lastname').style.border='solid';
        }
    }

    const name=document.getElementById("name");
    name.addEventListener("input",functionname);

    function functionname(e) {
        if (e.target.value.length<5){
            document.getElementById('name').style.borderColor='#e52213';
           // alert("problem w name")
        }else {
            document.getElementById('name').style.border='solid';
        }
    }

    const loigin= document.getElementById("login");
    login.addEventListener("input", functionlogin);

    function functionlogin(e) {
        if (e.target.value.length<5){
            document.getElementById('login').style.borderColor='#e52213';
            // alert("problem w name")
        }else {
            document.getElementById('login').style.border='solid';
        }
    }

});