var btnStudy = document.getElementsByClassName('btn')[0];
var btnSports = document.getElementsByClassName('btn')[1];
var btnFriends = document.getElementsByClassName('btn')[2];
var btnTodolist = document.getElementsByClassName('btn')[3];
var list = document.getElementById('container');
var $tasksList = $("#tasksList");
var $notification = $("#notification");


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

btnTodolist.addEventListener('mouseup', function(e){
	mouseX = e.clientX;
	mouseY = e.clientY;
	
	displayList();
});


var displayList = function() {
	list.style.display = "block";
	var htmlStr = "";
    //从服务器端获取的数组
    $.ajax({
        async: true,
        url: "/ShowToDoList",
		type: "POST",
        dataType: "json",
        success: function (redata) {
			var index = 0;
			var htmlStr="";
			for(var d in redata.data){
				htmlStr += "<li>" + redata.data[index] + "<button class='delete'><span><i class='fa fa-trash-o'></i></span></button></li>";
				index = index + 1;
	    	}
			$tasksList.html(htmlStr);
            if (!$tasksList.children().length) {
                //$notification.css("display", "block");
                $notification.fadeIn("fast");
            } else {
                $notification.css("display", "none")
            }
            $(".delete").on("click", function() {

                //Assigning "this" to varible, as it doesn't
                //work correctly with setTimeout() function
                var $parent = $(this).parent();
                
                var text = $parent.text();
                var data_to_delete = {"event" : text};
                senddata_delete = JSON.stringify(data_to_delete);
                $.ajax({
                    async: true,
                    url: "/RemoveFromToDo",
                    type: "POST",
                    data: senddata_delete,
                    dataType: "json",
                    success: function (redata) {
                     
                    }
                    }
                )
                //上传数据  $parent
                //Displaying CSS animation
                $parent.css("animation", "fadeOut .3s linear");

                //Timeout on remove function
                setTimeout(function() {
                    $parent.remove();
                    if (!$tasksList.children().length) {
                //$notification.css("display", "block");
                $notification.fadeIn("fast");
            } else {
                $notification.css("display", "none")
            }
        }, 295);

            });
		}
	}) 

    }
