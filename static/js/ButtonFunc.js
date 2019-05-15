var btnStudy = document.getElementsByClassName('btn')[0];
var btnSports = document.getElementsByClassName('btn')[1];
var btnFriends = document.getElementsByClassName('btn')[2];
var btnTodolist = document.getElementsByClassName('btn')[3];
var div = document.getElementById('background');
var close = document.getElementById('close-button');

var mouseX = window.innerWidth / 2;
var mouseY = window.innerHeight / 2;

btnStudy.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	div.style.display = "block";
});

btnSports.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;

});

btnFriends.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	
});

close.onclick = function close() {
	div.style.display = "none";
}
 
window.onclick = function close(e) {
	if (e.target == div) {
		div.style.display = "none";
	}
}
