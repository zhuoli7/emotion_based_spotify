"use strict";

var webApiBaseUrl = "https://api.spotify.com/v1/";
var artist;
var albums = [];
var favouriteSongs = [];

$('#search').on('click', function (e) {
	e.preventDefault();
	artist = $('#artist').val();
	$('#artist').val();
	searchArtist ();
});

$(document).keypress(function(e) {
	if(e.which == 13) {
		artist = $('#artist').val();
		$('#artist').val();
		searchArtist ();
	}
});

$(document).on('click', '#add', function (e) {
	e.preventDefault();
	var addButton = document.getElementById("add")
	var favouriteSong = $(this).data('name');
	var userName = window.localStorage.key(0);
	var favsSongs = JSON.parse(window.localStorage.getItem(userName));
	favsSongs.push(favouriteSong);	
	window.localStorage.setItem(userName, JSON.stringify(favsSongs));
});


$(window).on('load', function(){
	var userName = window.localStorage.key(0);
	if (window.localStorage.getItem(userName) != "[]"){
		var showFavs = "<button id='favs'>Favourite songs</button>";
		$( ".form" ).after(showFavs);
	}
});

$(document).on('click', '#favs', function (e){
	e.preventDefault();
	var userName = window.localStorage.key(0);
	var favouriteSongs = JSON.parse(window.localStorage.getItem(userName));
	var favouriteSongsList = '<ul id="favouriteSongsList"></ul>';	
	$('#favs').after(favouriteSongsList);

	for (var i = 0; i<favouriteSongs.length; i++){
		var favouriteSong = favouriteSongs[i];
		var favouriteSongLi = '<li id="' + favouriteSong + '">' + favouriteSong + '</li>';
		$('#favouriteSongsList').append(favouriteSongLi);
	}
});

function ajaxRequest(url, func1, func2){
	$.ajax({
		url: url, 
		dataType:"json",
		beforeSend:func1,
	}).done(func2)
	.fail(failFunction);
}

function searchArtist () {
	var searchArtistUrl = webApiBaseUrl + "search?q=" + artist + "&type=artist";
	var searchArtistLog = function () { console.log("searching artist")};

	ajaxRequest(searchArtistUrl, searchArtistLog, successSearchNameArtist);
}

function successSearchNameArtist (data) {

	//Tenemos el artista, cogemos el id del artista 
	//y hacemos una request de los álbumes /v1/artist/ID/albums
	//Sacar todos los nombres de álbumes y imagen. 
	//appendchild.
	$('.container .main #artist').empty();
	$('.container .main #albums').empty();
	$('.container .main #albumSongs').empty();
	var singer = data.artists.items[0].name;
	var artistId = data.artists.items[0].id;

	var searchArtistIdUrl = webApiBaseUrl + "artists/" + artistId + "/albums";
	var searchArtistLog = function () { console.log("searching artist by ID")};
	
	var followButton = '<iframe src="https://embed.spotify.com/follow/1/?uri=spotify:artist:'+ data.artists.items[0].id 
	+ '&size=detail&theme=light" width="300" height="56" scrolling="no" frameborder="0" style="border:none; overflow:hidden;" allowtransparency="true"></iframe>'

	$('.container .main #artist').append(followButton);

	ajaxRequest(searchArtistIdUrl, searchArtistLog, searchAlbum);
}

function searchAlbum (data) {

	for (var i = 0; i<data.items.length; i++){

		var albumName = data.items[i].name;
		var albumUrl = data.items[i].external_urls.spotify;
		var albumImage = data.items[i].images[2].url;

		var cover = '<div class="album img-thumbnail">' + '<h6>' + albumName + '</h6>' 
		+ '<a href="#" class="albumLink" data-name="' + albumName + '"><img width="100px" height="100px" src="' + albumImage + '" ></a>'

		$('#albums').append(cover);
	}
}

$(document).on('click', '.albumLink', function (e) {
	e.preventDefault();
	var albumToSearchTracks = encodeURI($(this).data('name'));
	searchAlbumTracks(albumToSearchTracks);
});

function failFunction(request, textStatus, errorThrown) {
	alert("An error occurred during your request: " + request.status + " " + textStatus + " " + errorThrown);
}


function searchAlbumTracks(albumName) {
	var uriToSearchAlbumId = webApiBaseUrl + "search?q=" + albumName + "&type=album";
	var searchAlbumId = function () { console.log("searching album ID")};
	ajaxRequest(uriToSearchAlbumId, searchAlbumId, queHacerCuandoTenemosElId);

}

function queHacerCuandoTenemosElId (data){
	$('.container .main #albumSongs').empty();
	var albumID = data.albums.items[0].id;
	var uriToSearchTracksOfTheAlbum = webApiBaseUrl + "albums/" + albumID + "/tracks";
	var searchingTracks = function () { console.log("searching tracks")};
	ajaxRequest(uriToSearchTracksOfTheAlbum, searchingTracks, pegameLasCanciones);
}

function pegameLasCanciones (data) {
	var albumSongList = '<ol class="albumSongsList"></ol>';
	$('#albumSongs').append(albumSongList)
	for (var i = 0; i<data.items.length; i++){
		var songName = data.items[i].name;
		var songUri = encodeURI(data.items[i].uri);
		var trackNumber = data.items[i].track_number;
		var songLi = '<li><iframe src="https://embed.spotify.com/?uri=' + songUri + '" data-name="' + songName + '" width="300" height="80" frameborder="0" allowtransparency="true"></iframe><button class="buttonAdd" type="submit" id="add" data-name="' + songName + '" >Añadir a favoritos</button></li>';
		$('.albumSongsList').append(songLi);
	}
}


