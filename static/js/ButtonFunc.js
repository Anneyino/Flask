var btnStudy = document.getElementsByClassName('btn')[0];
var btnSports = document.getElementsByClassName('btn')[1];
var btnFriends = document.getElementsByClassName('btn')[2];
var btnTodolist = document.getElementsByClassName('btn')[3];
var list = document.getElementById('container');
var tasksList = document.getElementById("tasksList");

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

btnTodolist.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	
	displayList();
});


var displayList = function() {
    list.style.display = "block";
    var htmlStr = "";
    //从服务器端获取的数组
    var temp = new Array(1,2,3);

    for(var i = 0;i < temp.length;i++){
    	htmlStr += "<li>" + temp[i] + "<button class='delete'><span><i class='fa fa-trash-o'></i></span></button></li>";
    }

    tasksList.innerHTML = htmlStr;
}
