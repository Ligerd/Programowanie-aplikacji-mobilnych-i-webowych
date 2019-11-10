$(document).ready(function () {
    
    $("#registration").click(function () {
        $.get( "http://localhost:3001/rejestracja", function( data ) {
        $( "body" ).html( data );
    });
    });

});