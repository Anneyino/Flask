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
		
        $('.sort_list').click(function(){
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
            alert($(this).innerHTML);
            var target_form = $(this).find('.gofriend');
            alert(target_form.innerHTML);
            console.log(target_form.innerHTML);
            target_form.submit();           

        });

		$('#search').bind('input propertychange', function() { 
			$('.sort_box-two').html('');
			 //进行相关操作 
			var val=$(this).val();
			if(val==""){
				return;
			}
			var str="";
			//去查找原字符串及其拼音首字母是否包含此字符，若包含就把它加进去
			$(".sort_list").each(function() {
				//var name=$(this).find('.num_name').text();   
				if(name.toLowerCase().indexOf(val.toLowerCase()) != -1){//包含
					str+="<div class='sort_list-two' id='"+$(this).attr('id')+"'> "+$(this).html()+"</div>";
				}else{
					var PYarr = makePy(name);
					for(var i=0;i<PYarr.length;i++){
						
						if(PYarr[i].toLowerCase().indexOf(val.toLowerCase()) != -1){//包含
							str+="<div class='sort_list-two' id='"+$(this).attr('id')+"'> "+$(this).html()+"</div>";
						}else{//不包含
							
						}
					}
				}
		        
		    });
			$('.sort_box-two').html(str);
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