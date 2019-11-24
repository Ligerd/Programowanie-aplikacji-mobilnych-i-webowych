$(document).ready(function () {

    $("#refresh").click(function () {
        $.ajax({
            url: "http://localhost:3000/files",
            type: "GET",
            success: function (data) {
                console.log(data['my_files']);
                   document.getElementById('lista').remove();
                   var ul=document.createElement('ul');
                   ul.setAttribute("id", "lista");
                   document.getElementById('myList').appendChild(ul);
                   data['my_files'].forEach(function(name){
			        var li = document.createElement('li');
			        var a=document.createElement('a');
			        var v="http://localhost:3000/download/"+name;
			        console.log(v);
			        a.setAttribute("href",v);
			        li.appendChild(a);
			        a.innerHTML += name;
			        ul.appendChild(li);
			        //li.innerHTML += name;
                });

            },
            error:function (error) {
                console.log("ERROR")
            }
        })
    })
});