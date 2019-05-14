var btnStudy = document.getElementsByClassName('btn')[0];
var btnSports = document.getElementsByClassName('btn')[1];
var btnFriends = document.getElementsByClassName('btn')[2];

var mouseX = window.innerWidth / 2;
var mouseY = window.innerHeight / 2;

btnStudy.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	
});

btnSports.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;

});

btnFriends.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	

});
