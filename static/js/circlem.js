function back(){
			$('[class*="-two"]').css('display','none');
			$('.sort_box').css('display','block');
			$('.initials').css('display','block');
			$('.header').css('display','block');
		}

$(function(){
		
		window.onresize=function(){
			if($(window).height()<400){
				$('.nav').hide();
			}else{
				$('.nav').show();
			}
			 
		}
		$('[class*="-two"]').css('display','none'); 
		$('#gosearch').click(function(){
			
			$('[class*="-two"]').css('display','block');
			$('.sort_box').css('display','none');
			$('.header').css('display','none');
			$('.initials').css('display','none');
			$('#search').focus();
			
		});
        
         //取消关注按钮
         $('.focus_btn').click(function(){
          var friendname = $(this).prev().val()  
          var form_remove = $(this).parent();
          var remove_friend = confirm("是否取消对"+friendname+"的关注？");
          if(remove_friend==true){
           form_remove.submit();
          }else{
              return;
          }

        });

        //关注按钮
        $('.focus_btn-two').click(function(){
          var parentForm = $(this).parent();
          if($(this).text()=="未关注"){
              parentForm.submit();
          }else{
              var friendname = $(this).prev().val()
              var remove_friend = confirm("是否取消对"+friendname+"的关注？");
              if(remove_friend == true){
              parentForm.submit();
              }else{
                  return;
              }

          }
            
        });
		
        $('.num_name').click(function(){
            /*var friendname = $(this).text();
            var data_friend = { "friend_name" : friendname };
            senddata_friend = JSON.stringify(data_friend);
            $.ajax({
                async: false,
                url: "/GoForFriend",
                type: "POST",
                data: senddata_friend,
                dataType: "json",
                success: function (data) {
                alert(data.fid);
              }
             })*/
            var target_form = $(this).parent();
            target_form.submit();           

        });

        $('#search').bind('input propertychange', function() { 
            $('.sort_box-two').html('');
             //进行相关操作 
            var val=$(this).val();
            if(val==""){
                return;
            }
            var data = {"Searchkeyword" : val};
            senddata = JSON.stringify(data);            
            $.ajax({
                async: true,
                url: "/searchUser",
                type: "POST",
                data: senddata,
                dataType: "json",
                success: function (redata) {
                    var index = 0;
                    var htmlstr="";

                    for(var d in redata.data){
                        htmlstr += '<div class = "sort_list-two">' +
                        '<form class = "gofriend" action = "/GoForFriend" method = "POST">' +
                        '<div class = "num_name">' + redata.data[index] + '</div>' +
                        '<input type="text" id="fname" name="fname" value ='+ redata.data[index] +' style="display:none;"/>' +
                        '</form>'+
                        '<form class = "losefocusfriend" action = '+ redata.action[index] +' method = "POST">' +
                        '<input type="text" id="uid" name="uid" value =' + redata.data[index] + ' style="display:none;"/>' +
                        '<button type="submit" class="focus_btn-two">'+ redata.isfriend[index] +'</button>' +
                        '</form>' +
                        '</div>';
                        index = index + 1;
                 }
                 $('.sort_box-two').html(htmlstr);  
                }
            }) 
        });

        var Initials=$('.initials');
        var LetterBox=$('#letter');
        Initials.find('ul').append('<li>A</li><li>B</li><li>C</li><li>D</li><li>E</li><li>F</li><li>G</li><li>H</li><li>I</li><li>J</li><li>K</li><li>L</li><li>M</li><li>N</li><li>O</li><li>P</li><li>Q</li><li>R</li><li>S</li><li>T</li><li>U</li><li>V</li><li>W</li><li>X</li><li>Y</li><li>Z</li><li>#</li>');
        initials();

        $(".initials ul li").click(function(){
            var _this=$(this);
            var LetterHtml=_this.html();
            LetterBox.html(LetterHtml).fadeIn();

            Initials.css('background','rgba(145,145,145,0.6)');
            
            setTimeout(function(){
                Initials.css('background','rgba(145,145,145,0)');
                LetterBox.fadeOut();
            },1000);

            var _index = _this.index()
            if(_index==0){
                $('html,body').animate({scrollTop: '0px'}, 300);//点击第一个滚到顶部
            }else if(_index==27){
                var DefaultTop=$('#default').position().top;
                $('html,body').animate({scrollTop: DefaultTop+'px'}, 300);//点击最后一个滚到#号
            }else{
                var letter = _this.text();
                if($('#'+letter).length>0){
                    var LetterTop = $('#'+letter).position().top;
                    $('html,body').animate({scrollTop: LetterTop-45+'px'}, 300);
                }
            }
        })

        var windowHeight=$(window).height();
        var InitHeight=windowHeight-45;
        Initials.height(InitHeight);
        var LiHeight=InitHeight/28;
        Initials.find('li').height(LiHeight);
})

function initials() {//公众号排序
    var SortList=$(".sort_list");
    var SortBox=$(".sort_box");
    SortList.sort(asc_sort).appendTo('.sort_box');//按首字母排序
    function asc_sort(a, b) {
        return makePy($(b).find('.num_name').text().charAt(0))[0].toUpperCase() < makePy($(a).find('.num_name').text().charAt(0))[0].toUpperCase() ? 1 : -1;
    }

    var initials = [];
    var num=0;
    SortList.each(function(i) {
        var initial = makePy($(this).find('.num_name').text().charAt(0))[0].toUpperCase();
        if(initial>='A'&&initial<='Z'){
            if (initials.indexOf(initial) === -1)
                initials.push(initial);
        }else{
            num++;
        }
        
    });

    $.each(initials, function(index, value) {//添加首字母标签
        SortBox.append('<div class="sort_letter" id="'+ value +'">' + value + '</div>');
    });
    if(num!=0){SortBox.append('<div class="sort_letter" id="default">#</div>');}

    for (var i =0;i<SortList.length;i++) {//插入到对应的首字母后面
        var letter=makePy(SortList.eq(i).find('.num_name').text().charAt(0))[0].toUpperCase();
        switch(letter){
            case "A":
                $('#A').after(SortList.eq(i));
                break;
            case "B":
                $('#B').after(SortList.eq(i));
                break;
            case "C":
                $('#C').after(SortList.eq(i));
                break;
            case "D":
                $('#D').after(SortList.eq(i));
                break;
            case "E":
                $('#E').after(SortList.eq(i));
                break;
            case "F":
                $('#F').after(SortList.eq(i));
                break;
            case "G":
                $('#G').after(SortList.eq(i));
                break;
            case "H":
                $('#H').after(SortList.eq(i));
                break;
            case "I":
                $('#I').after(SortList.eq(i));
                break;
            case "J":
                $('#J').after(SortList.eq(i));
                break;
            case "K":
                $('#K').after(SortList.eq(i));
                break;
            case "L":
                $('#L').after(SortList.eq(i));
                break;
            case "M":
                $('#M').after(SortList.eq(i));
                break;
            case "O":
                $('#O').after(SortList.eq(i));
                break;
            case "P":
                $('#P').after(SortList.eq(i));
                break;
            case "Q":
                $('#Q').after(SortList.eq(i));
                break;
            case "R":
                $('#R').after(SortList.eq(i));
                break;
            case "S":
                $('#S').after(SortList.eq(i));
                break;
            case "T":
                $('#T').after(SortList.eq(i));
                break;
            case "U":
                $('#U').after(SortList.eq(i));
                break;
            case "V":
                $('#V').after(SortList.eq(i));
                break;
            case "W":
                $('#W').after(SortList.eq(i));
                break;
            case "X":
                $('#X').after(SortList.eq(i));
                break;
            case "Y":
                $('#Y').after(SortList.eq(i));
                break;
            case "Z":
                $('#Z').after(SortList.eq(i));
                break;
            default:
                $('#default').after(SortList.eq(i));
                break;
        }
    };
}