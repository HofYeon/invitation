let WIN_SCR_TOP = 0


// 축하화환
function floatGarland() {
    $(".floatingBox").addClass("see animated animate__fadeInUp");
    setTimeout(function(){
        $(".floatingBox").toggleClass("hi");
    }, 2000);
}
// 열기
document.querySelector(".floatingBox, .garlandSection .garBox")?.addEventListener('click', () => {
    $(".bttmGarlandWrapper .in").removeClass("animate__fadeOutDown");
    $(".bttmGarlandWrapper").addClass("see");
    $(".bttmGarlandWrapper .in").addClass("animated animate__fadeInUp");
});
// 닫기
$(".bttmGarlandWrapper .close").click(function(){

    $(".bttmGarlandWrapper").removeClass("see");
    $(".bttmGarlandWrapper .in").addClass("animate__fadeOutDown");

});


function openContactPop() {
    $("body").addClass("pop_contact_open");
    const top = document.querySelector('html').scrollTop;
    WIN_SCR_TOP = top;
    $("html,body").css("overflow", "hidden");
}
function openInterviewPop() {
    $("body").addClass("pop_interview_open");
    const top = document.querySelector('html').scrollTop;
    WIN_SCR_TOP = top;
    $("html,body").css("overflow", "hidden");
}

function youtube_parser(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}


// BGM 애니메이션 효과
function bgmAniFunc() {
    $('.anibox2').addClass("hd").viewportChecker({
        classToAdd: 'visible animated fadeInDown ',
        offset: 0,
        callbackFunction: function(elem, action) {
            setTimeout(function(){
                $(".bgmbar").addClass("fadeBg");
            }, 2500);
        }
    });

    var videocontrol = document.getElementById("videoplay");
    if(!(videocontrol?.paused)) {
        $(".bgmbar .sound").find("i.fa").removeClass("fa-volume-off");
        $(".bgmbar .sound").find("i.fa").addClass("fa-volume-up");
    }
}



// 계좌번호 팝업
let isAcctBox = false
function openAcctBox(i) {
    $("#acctBox .grp").text($(i).attr("data-group"));
    $("#acctBox .ment").html($(i).attr("data-bank")+"<br/>"+$(i).attr("data-number")+"<br/>"+$(i).attr("data-name"));
    $("#copytext").val($(i).attr("data-number"));
    $("#acctBox").css("display", "block");
    isAcctBox = true
}
function closeAcctBox() {
    $("#acctBox").css("display", "none");
}

// 클립보드 복사 기능
function copy_to_clipboard(txtId) {
	/*var copyText = document.getElementById(txtId);
	copyText.select();
	document.execCommand("Copy");
    remove_focus_clipboard();
    alert("복사가 완료되었습니다.");*/

    var copytxt = $("#"+txtId).val();
    const t = document.createElement("textarea");
    document.body.appendChild(t);
    t.value = copytxt;
    t.select();
    document.execCommand('copy');
    document.body.removeChild(t);
    // alert("복사가 완료되었습니다.");
    document.querySelector(`.acc_copy`).style.display = 'block'
    document.querySelector(`#acctBox`).style.display = 'none'
}
function copy_to_clipboard2(txtId) {
    /*var copyText = document.getElementById(txtId);
	copyText.select();
	document.execCommand("Copy");
    remove_focus_clipboard();
    alert("복사가 완료되었습니다.");*/

    var copytxt = $("#"+txtId).val();
    const t = document.createElement("textarea");
    document.body.appendChild(t);
    t.value = copytxt;
    t.select();
    document.execCommand('copy');
    document.body.removeChild(t);
    // alert("복사가 완료되었습니다.");
    const msg = lang === 'ko' ? '복사가 완료되었습니다.' : 'Copied successfully.'
    openAlert(msg)
    document.querySelector(`.acc_copy`).style.display = 'block'
}

function remove_focus_clipboard() {

    var sel = window.getSelection ? window.getSelection() : document.selection;
    if (sel) {
        if (sel.removeAllRanges) {
            sel.removeAllRanges();
        } else if (sel.empty) {
            sel.empty();
        }
    }
/*
    if (window.getSelection) {
        if (window.getSelection().empty) {  // Chrome
            window.getSelection().empty();
        } else if (window.getSelection().removeAllRanges) {  // Firefox
            window.getSelection().removeAllRanges();
        }
    } else if (document.selection) {  // IE?
        document.selection.empty();
    }
*/
}






//


/*
var map = null;
var marker = null;
*/

function searchDirCoord(x, y) {

    var point = new naver.maps.Point(x, y);

    NAVER_MAP = new naver.maps.Map("map", {
        center: point,
        zoom: 16,
        mapTypeControl: false,
        anchorSkew: true
    });
    //map.setCenter(point);
    marker = new naver.maps.Marker({
        position: point,
        map: NAVER_MAP
    });

}

function searchAddressToCoordinate(address) {

    /*var cod = null;
    if(address == "서울 송파구 양재대로 932 가락몰 SAFF타워 (업무동)") {
        cod = "SAFF타워 (업무동) 2F";
    }*/

    naver.maps.Service.geocode({
        query: address
    }, function(status, response) {

        //console.log(status);
        //console.log(response);

        if (status === naver.maps.Service.Status.ERROR) {
            //return console.log('Something Wrong!');
            return;
        }

        if (response.v2.meta.totalCount === 0) {
            //return console.log('totalCount' + response.v2.meta.totalCount);
            return;
        }

        var htmlAddresses = [],
            item = response.v2.addresses[0],
            point = new naver.maps.Point(item.x, item.y);


        if (item.roadAddress) {
            htmlAddresses.push('[도로명 주소] ' + item.roadAddress);
        }

        if (item.jibunAddress) {
            htmlAddresses.push('[지번 주소] ' + item.jibunAddress);
        }

        if (item.englishAddress) {
            htmlAddresses.push('[영문명 주소] ' + item.englishAddress);
        }

        /*infoWindow.setContent([
            '<div class="ft02" style="padding:10px;min-width:200px;line-height:150%;">',
            '<h4 style="font-size: 16px;padding: 0px;">'+ gWeddingAddr +'</h4><br />',
            //htmlAddresses.join('<br />'),
            '</div>'
        ].join('\n'));*/

        NAVER_MAP = new naver.maps.Map("map", {
            center: point,
            zoom: 16,
            mapTypeControl: false,
            anchorSkew: true
        });
        //map.setCenter(point);
        marker = new naver.maps.Marker({
            position: point,
            map: NAVER_MAP
        });


        //infoWindow.open(map, point);
    });
}






function fnCallWeb2App(type) {
    event.preventDefault();
    var scheme, package, fallbackUrl, fail, useUrlScheme;
    const msg = lang === 'ko' ? '앱이 설치되어 있지 않은 경우\n길 안내가 실행되지 않을 수 있습니다' : 'If the app is not installed, directions may not start.'

    switch(type) {
        case 'kakaoNavi':
            openAlert(msg);
            /*window.open('https://map.kakao.com/link/to/서울 신라호텔,37.5575055053737,127.007952910656','kakaomap','');*/
            Kakao.Navi.share({
                name: mp_hname,
                x: mp_x,
                y: mp_y,
                coordType: 'wgs84'
            });
            break;
        case 'tmap':
            openAlert(msg);
            scheme = `tmap://route?goalx=${mp_x}&goaly=${mp_y}&goalname=${mp_hname}`;
            package = 'com.skt.tmap.ku';
            fallbackUrl = scheme;
            break;
        case 'naverMap':
            openAlert(msg);
            scheme = `navermaps://?menu=location&pinType=place&lat=${mp_y}&lng=${mp_x}&title=${mp_hname}`;
            package = 'com.nhn.android.nmap';
            //useUrlScheme = true;
            fallbackUrl = `http://map.naver.com/index.nhn?elng=${mp_x}&elat=${mp_y}&etext=${mp_hname}&menu=route&pathType=0`;
            fail = function() {
                $('#fakeAnchor').remove();
                $('body').append(`<a href='http://map.naver.com/index.nhn?elng=${mp_x}&elat=${mp_y}&etext=${mp_hname}&menu=route&pathType=0' id='fakeAnchor'></a>`);
                $('#fakeAnchor').get(0).click();
            }
            break;

    }

    const callWeb2App = new CallWeb2App({
        scheme: scheme,
        package: package,
        useUrlScheme: useUrlScheme,
        fallbackUrl: fallbackUrl,
        fail: fail
    });

    callWeb2App.run();
}

const moreInterview = () => {
    document.querySelectorAll('#interview_pop ul.interview li').forEach(item => item.style.display = '')
    document.querySelector(`#interview_pop .more`).style.display = 'none'
}


const moreBooks = (ele) => {
    document.querySelectorAll(`.books-open-list-ul li:not(.on)`).forEach((item, key) => {
        if(key < 4) {
            item.classList.add('on')
        }
    })
    if(document.querySelectorAll(`.books-open-list-ul li:not(.on)`).length == 0) {
        ele.style.display = 'none'
    }
}

// 안내사항 이미지 팝업
const openInfoPopup = (imgPath) => {
    $(".pageCover").addClass("blur6");
    $(".popNoticeImg").addClass("visible");

    document.querySelector(`#popNoticeImgWrap img`).src = imgPath
}


/**
 * [BGM 스트리밍 재생, 정지]
 */
const bgmStreaming = () => {
    if(typeof isPlay !== 'undefined' && isPlay) {
        const bgm = document.querySelector('#videoplay');
        const url = bgm.getAttribute('data-url')
        if(url.includes('mp3')) {
            if(bgm.paused) {
                bgm.play()
            }
        } else {
            bgm.setAttribute('type', 'application/x-mpegURL')

            if(!Hls.isSupported() && bgm.canPlayType('application/vnd.apple.mpegurl') === 'maybe') {
                bgm.src = url
                if(bgm.paused) {
                    bgm.play()
                }
            } else {
                const hls = new Hls()
                hls.loadSource(url)
                hls.attachMedia(bgm)
                if(bgm.paused) {
                    bgm.play()
                }
            }
        }

        if(bgm.paused) {
            $(".bgmbar .sound").find("i.fa").addClass("fa-volume-off");
            $(".bgmbar .sound").find("i.fa").removeClass("fa-volume-up");
        } else {
            $(".bgmbar .sound").find("i.fa").removeClass("fa-volume-off");
            $(".bgmbar .sound").find("i.fa").addClass("fa-volume-up");
        }
    }
}
