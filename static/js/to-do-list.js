        document.addEventListener('touchstart', function() {}, true);
        $(document).on("touchend", "li", function() {
            $(this).toggleClass("completed");
        });
        $(function() {
            //Attaching DOM element to varibles
            var $tasksList = $("#tasksList");
            var $taskInput = $("#taskInput");
            var $notification = $("#notification");

            //Counting amount of items in the list
            //To display or hide notification
            var displayNotification = function() {
                if (!$tasksList.children().length) {
                    //$notification.css("display", "block");
                    $notification.fadeIn("fast");
                } else {
                    $notification.css("display", "none")
                }
            }

            //Attaching event handler to add button
            $("#taskAdd").on("click", function() {

                //Returning false if input is empty
                if (!$taskInput.val()) {
                    return false;
                }

                //Appending li with input value
                $tasksList.append("<li>" + $taskInput.val() + "<button class='delete'><span><i class='fa fa-trash-o'></i></span></button></li>");

                //Cleaning input after add
                $taskInput.val("");

                //Display/Hide Notification
                displayNotification();

                //Attaching even handler to delete button
                $(".delete").on("click", function() {

                    //Assigning "this" to varible, as it doesn't
                    //work correctly with setTimeout() function
                    var $parent = $(this).parent();

                    //Displaying CSS animation
                    $parent.css("animation", "fadeOut .3s linear");

                    //Timeout on remove function
                    setTimeout(function() {
                        $parent.remove();
                        displayNotification();
                    }, 295);

                })
            })
        });