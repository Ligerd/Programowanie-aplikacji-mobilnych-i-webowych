$(document).ready(function () {
        $("#login").blur(function () {
        $.ajax({
            type : 'POST',
            url : 'http://localhost:3000/rejestracja',
            data :{
                login : $("#login").val()
            }
        })
            .done(function (data) {
                if(data.error){
                    $("#login").css("color","red");
                    document.getElementById("login-error").innerHTML = data.error;
                }else {
                    $("#login").css('color', 'green');
                    document.getElementById("login-error").innerHTML='';

                }
            });
        event.preventDefault();
    });
});