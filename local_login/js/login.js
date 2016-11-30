"use strict";
var name;
var pass;

//$(document).on('click', "#login", clickJson());

$('#login').on('click', function (e) {
	e.preventDefault();
	name = $('#name').val();
	pass = $('#password').val();

	$('#name').val("");
	$('#password').val("");

	getUsersList ();


});
/*
function searchOnEnter(e){
	e = e || window.event;
	if (e.keyCode == 13) {
		name = $('#name').val();
		pass = $('#password').val();

		$('#name').val("");
		$('#password').val("");

		getUsersList ();
		return false;
	}
	return true;
};*/

function getUsersList () { //Aquí chequeamos el usuario y la contraseña.

	$.ajax({
    crossDomain: true,
    url: 'js/json_Users.jsonp',
    dataType: 'jsonp',
    method: "GET",
    jsonpCallback: 'usersData',
    contentType: 'application/jsonp',
    success: success,
    error: error
});
}

function success (jsonp) {

	var ok = false


	for (var i = 0; i<jsonp.users.length; i++){
		if(name === jsonp.users[i].name && pass === jsonp.users[i].pass) {
			
			ok = true;
		}
		}
	if (ok === true) {
		window.location.href="spoty.html";
		console.log("user and pass ok")
		var userName = name;
		var list = [];
		window.localStorage.setItem(name, JSON.stringify(list));
	} else {
		alert("user not found")
	}

};

function error (request, textStatus, errorThrown) {
        	alert(request.status + " "+ textStatus + ': ' + errorThrown);
};

