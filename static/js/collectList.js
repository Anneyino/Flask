$(document).ready(function() {
    var check_count = 0;
    var total = 0;
    var timeout;
    $('ul').add(function(e){
                
    });
    // Get the total number of "li's" and checked "li's"
    $('li').each(function(e) {
        total++;
        $('#count').text(total);
        var findTheMarkedList = $(this);

        if (findTheMarkedList.find('i').hasClass('fa fa-check-circle mark')) {
            let checkIfmarked = $('li .check_button').index(this);
            $('li .right').eq(checkIfmarked).find('p').addClass('line-through').attr("contentEditable", false);
            check_count++;
            $('#count_done').text(check_count);
        }
        $('#remaining_done').text(total - check_count);
    });
    

    //返回按钮
    $('.bottom a').click(function(e) {
    });
    // Click on button function list
    $('.app ul').on('click', 'li .check_button', function(e) {
        e.preventDefault();
        let button = $(this).find('i');
        let checked = 'fa fa-check-circle mark';
        let unchecked = 'fa fa-circle-thin';

        // Save the current index of button after the click event in the "left" div.
        let index_click = $('li .check_button').index(this);
        // Use the current index of button to target the correct "li p" in the "right" div.
        let linethrough_text = $('li .right').eq(index_click).find('p');

        if (button.hasClass(unchecked)) {
            linethrough_text.addClass('line-through').attr("contentEditable", false);
            button.removeClass(unchecked + ' mark-alt').addClass(checked);
            check_count += 1;
        } else {
            linethrough_text.removeClass('line-through').attr('contentEditable', true);
            button.removeClass(checked).addClass(unchecked + ' mark-alt');
            check_count -= 1;
        }

        $('#count_done').text(check_count);
        $('#remaining_done').text(total - check_count);
    });
    // Click on button function and delete 'li'
    $('.app ul').on('click', 'li .delete_button', function(e) {
        e.preventDefault();
        let index_click = $('li .delete_button').index(this);
        let current = $('li').eq(index_click);
        let button = $('ul li .check_button').find('i');

        total -= 1;
        $('#count').text(total);

        if (button.eq(index_click).hasClass('mark')) {
            check_count -= 1;
            $('#count_done').text(check_count);
        }
        current.addClass('up');
        setTimeout(function() {
            current.remove();
        }, 600);
        $('#remaining_done').text(total - check_count);
    });

    var suffix = "";
    var date = new Date();
    var dayOfMonth = date.getDate();
    var dayOfWeek = date.getDay();
    var Month = date.getMonth();

    var dayArray = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var monthArray = ["January", "February", "March", "April,", "May", "June", "July", "August", "September", "October", "November", "December"];
    switch (dayOfMonth) {
        case (dayOfMonth == 1 || dayOfMonth == 21 || dayOfMonth == 31):
            suffix = 'st';
            break;
        case (dayOfMonth == 2 || dayOfMonth == 22):
            suffix = 'nd';
            break;
        case (dayOfMonth == 3 || dayOfMonth == 23):
            suffix = 'rd';
            break;
        default:
            suffix = 'th';
    }
    $('.app .info .date').append("<p id='day'><strong>" + dayArray[dayOfWeek] + ",</strong> " + dayOfMonth + suffix + "</p>" +
        "<p id='month'>" + monthArray[Month] + "</p>");

});