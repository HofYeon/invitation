var check = {
	isNotNull : function(v){
	    if ( typeof v == "undefined" || v == null || v ==""){
	        return false;
	    }else {
	        return true;
	    }
	},
	isBirthday : function(dateStr) {

		var year = Number(dateStr.substr(0,4)); // 입력한 값의 0~4자리까지 (연)
		var month = Number(dateStr.substr(4,2)); // 입력한 값의 4번째 자리부터 2자리 숫자 (월)
		var day = Number(dateStr.substr(6,2)); // 입력한 값 6번째 자리부터 2자리 숫자 (일)
		var today = new Date(); // 날짜 변수 선언
		var yearNow = today.getFullYear(); // 올해 연도 가져옴
		if (dateStr.length <=8) {
			if (1900 > year || year > yearNow){ return false; }
			else if (month < 1 || month > 12) { return false; }
			else if (day < 1 || day > 31) { return false; }
			else if ((month==4 || month==6 || month==9 || month==11) && day==31) { return false; }
			else if (month == 2) {
				var isleap = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
				if (day>29 || (day==29 && !isleap)) {
					return false;
				} else {
					return true;
				} //end of if (day>29 || (day==29 && !isleap))
			}
			else {
				return true;
			}
		}
		else {
			// 8자 초과시
			return false;
		}
	},

	// 이메일 유효성 검사
	isEmail : function(e){
		var regEmail = /([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
		return regEmail.test(e);
	},
	// 휴대전화 유효성 검사
	isCellPhone : function(p){
		var regPhone = /^((01[1|6|7|8|9])[1-9]+[0-9]{6,7})|(010[1-9][0-9]{7})$/;
		return regPhone.test(p);
	},
	// 아이디 검사(영문소문자,숫자로만 이루어진)
	isId : function(e) {
		var idReg = /^[a-z]+[a-z0-9]{3,19}$/g;
	    if(!idReg.test(e)) {
	        console.log("아이디는 영문자로 시작하는 6~20자 영문자 또는 숫자이어야 합니다.");
	        return false;
	    }
	    return true;
	},
	// 비밀번호 검사
	isPassword : function(str){
		var pw = str;
		var num = pw.search(/[0-9]/g);
		var eng = pw.search(/[a-z]/ig);
		var spe = pw.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);

		if(pw.length < 8 || pw.length > 20){
			console.log("8자리 ~ 20자리 이내로 입력해주세요.");
			return false;
		}
		if(pw.search(/₩s/) != -1){
			console.log("비밀번호는 공백업이 입력해주세요.");
			return false;
		}
		if(num < 0 || eng < 0 || spe < 0 ){
			console.log("영문,숫자, 특수문자를 혼합하여 입력해주세요.");
			return false;
		}
		return true;
	}
}


$.fn.serializeObject = function(){
    var obj = {};

    $.each( this.serializeArray(), function(i,o){
        var n = o.name,
        v = o.value;

        obj[n] = obj[n] === undefined ? v
            : $.isArray( obj[n] ) ? obj[n].concat( v )
            : [ obj[n], v ];
    });

    return obj;
};

function isMobile() {
	var UserAgent = navigator.userAgent;
	// 모바일 일때
	if (UserAgent.match(/iPhone|iPod|iPad|Android|Windows CE|BlackBerry|Symbian|Windows Phone|webOS|Opera Mini|Opera Mobi|POLARIS|IEMobile|lgtelecom|nokia|SonyEricsson/i) != null || UserAgent.match(/LG|SAMSUNG|Samsung/) != null){
		return true;
	}
	return false;
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


//부드럽게 레이어 이동
function moveLayer(idName) {
	var scrollPosition;

	if(!$("#header").hasClass("nonefix")) {
		scrollPosition = $("#"+idName).offset().top - 85;
	}else{
		scrollPosition = $("#"+idName).offset().top;
	}

	$("html, body").animate({scrollTop: scrollPosition}, 250);
}


// 클립보드 복사 기능
function copy_to_clipboard(txtId) {
	var copyText = document.getElementById(txtId);
	copyText.select();
	document.execCommand("Copy");
}

function openPop(id){

	$("#"+id).css("display", "block");
	//$("html,body").css("height", "100%");
	//$("html,body").css("overflow", "hidden");
	//$("html,body").css("position", "relative");
}
function closePop() {
	//$(".background_black_cover").css("display", "none");
	//$(".popup_layer").css("display", "none");

	$(".pop_wrapper").css("display","none");

	//$("html,body").css("height", "");
	//$("html,body").css("overflow", "");
	//$("html,body").css("position", "");
}

function closePrivacy(flag) {

	if(flag) {
		$("input[name=privacy_agreement]").prop('checked', true);
	}else{
		$("input[name=privacy_agreement]").prop('checked', false);
	}


    $(".pop_wrapper").css("display","none");

	$("html,body").css("height", "");
	$("html,body").css("overflow", "");
	$("html,body").css("position", "");

	var scrollPosition = $("#rd001112222").offset().top - 85;
	$("html, body").animate({scrollTop: scrollPosition}, 250);
}

function getPriceWithComma(values){
	values = parseInt(values);
	values = String(values);
    return values.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}
function adjustAmountComma(className) {
	$("."+className).each(function(){
		var data = $(this).text();
		console.log(data.indexOf(","));
		if(data.indexOf(",") == -1) {
			data = getPriceWithComma(data);
			$(this).text(data);
		}
	});
}

var hsdate = {
	getToday : function() {
		var d = new Date();
	    var s =
	        leadingZeros(d.getFullYear(), 4) + '-' +
	        leadingZeros(d.getMonth() + 1, 2) + '-' +
	        leadingZeros(d.getDate(), 2);

	    return s;
	},
	getYesterday : function() {
		var d = new Date();
		var y = d.getTime() - (1 * 24 * 60 * 60 * 1000);
		d.setTime(y);
		var s =
	        leadingZeros(d.getFullYear(), 4) + '-' +
	        leadingZeros(d.getMonth() + 1, 2) + '-' +
	        leadingZeros(d.getDate(), 2);

	    return s;
	}
}

function leadingZeros(n, digits) {

    var zero = '';
    n = n.toString();

    if (n.length < digits) {
        for (i = 0; i < digits - n.length; i++)
            zero += '0';
    }
    return zero + n;
}


//[쿠키관련]
var cookie = {

	// 저장된 쿠키를 가져온다.
	getCookie : function(name) {
		var Found = false
		var start, end
		var i = 0
		while(i <= document.cookie.length) {
			start = i
			end = start + name.length
			if(document.cookie.substring(start, end) == name) {
				Found = true
				break
			}
			i++
		}
		if(Found == true) {
			start = end + 1
			end = document.cookie.indexOf(";", start)
			if(end < start)
				end = document.cookie.length
			return document.cookie.substring(start, end)
		}
		return ""
	},
	// 쿠키를 저장한다.
	setCookie : function(name, value, expiredays){

		var endDate = new Date();
		endDate.setDate(endDate.getDate()+expiredays);
		document.cookie = name + "=" + escape(value) + "; path=/; expires=" + endDate.toGMTString() + ";";

	}

}

function getCurrentBrowser() {
	var agent = window.navigator.userAgent.toLowerCase();
	var browserName;
	switch (true) {
        case agent.indexOf("edge") > -1:
			browserName = "MS Edge"; // MS 엣지
			break;
		case agent.indexOf("edg/") > -1:
			browserName = "Edge (chromium based)"; // 크롬 기반 엣지
			break;
		case agent.indexOf("opr") > -1 && !!window.opr:
			browserName = "Opera"; // 오페라
			break;
		case agent.indexOf("chrome") > -1 && !!window.chrome:
			browserName = "Chrome"; // 크롬
			break;
		case agent.indexOf("trident") > -1:
			browserName = "MS IE"; // 익스플로러
			break;
		case agent.indexOf("firefox") > -1:
			browserName = "Mozilla Firefox"; // 파이어 폭스
			break;
		case agent.indexOf("safari") > -1:
			browserName = "Safari"; // 사파리
			break;
		default:
			browserName = "other"; // 기타
	}
	return browserName;
}


function goMypage() {
	var width_size = window.outerWidth;
    if (width_size >= 1000) {
        h = "/my/card";
    }else{
		h = "/my";
	}
	location.href=h;
}