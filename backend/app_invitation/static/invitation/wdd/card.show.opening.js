/*
    G-변수
*/
let G_ANI_LTT_OBJ = null;

// 오프닝애니메이션 동작
function activateSplash(splashType, isBgm, isGarland) {

    offScroll()
    if(splashType=="v1")
    {
        splash_v1(isBgm, isGarland);
    }
    else if(splashType=="v2")
    {
        var newImage0 = $(".ltt_wrapper .opening_v2_bg .img_01").attr("src");
        var newImage1 = $(".ltt_wrapper .opening_v2_bg .img_02").attr("src");
        var imagesLoaded = 0; // 로드된 이미지 개수
        console.log(newImage0);
        // 이미지 로드 확인 함수
        function checkImagesLoaded() {
            imagesLoaded++;
            if (imagesLoaded === 2) { // 모든 이미지가 로드되면
                splash_v2(isBgm, isGarland); // 애니메이션 시작
            }
        }

        // 첫 번째 이미지 로드 확인
        var img0 = new Image();
        img0.src = newImage0;
        img0.onload = checkImagesLoaded;

        // 두 번째 이미지 로드 확인
        var img1 = new Image();
        img1.src = newImage1;
        img1.onload = checkImagesLoaded;

    }
    else if(splashType=="v3")
    {
        splash_v3(isBgm, isGarland); // 애니메이션 시작
    }
}

//-----------------------------------------------------------------------------------------

// 오프닝 동작 중단(V1,V2,V3 해당) - 편집툴에서만 사용
function offSplash() {

    if(G_ANI_LTT_OBJ!=null) {
        G_ANI_LTT_OBJ.stop();
        G_ANI_LTT_OBJ.destroy();
        G_ANI_LTT_OBJ = null;
    }

    // V1 동작 멈춤
    const v1 = document.querySelector(".splash");
    if(v1) { v1.style.display = 'none'; }

    // V2~3 동작 멈춤
    const v2_3 = document.querySelector(".ltt_wrapper");
    if(v2_3) { v2_3.style.display = 'none'; }
}

// 오프닝 동작 후 스크롤 할 수 있도록 처리
function onScroll() {

    const viewer = document.querySelector(`#card_viewer`) // 편집페이지 확인
    if(viewer) {
        viewer.style.overflowY = ''
    } else {
        document.body.style.overflowY = ''
        document.body.style.height = ''
        document.body.style.width = ''
        document.body.style.position = ''
    }
}

// 오프닝 동작 중 스크롤 금지
function offScroll() {
    const viewer = document.querySelector(`#card_viewer`) // 편집페이지 확인
    if(viewer) {
        viewer.style.overflowY = 'hidden'
    } else {
        document.body.style.overflowY = 'hidden'
        document.body.style.height = '100%'
        document.body.style.width = '100%'
        document.body.style.position = 'fixed'
    }
}

// 오프닝 V1 (이전 함수이름 : splashAniFunc)
function splash_v1(isBgm, isGarland) {

    //$(".splash").css("display", "block");
    $(".pageCover").addClass("blur");

    var typingBool = false;
    var typingIdx=0;
    var typingTxt = $(".typing-txt").text(); // 타이핑될 텍스트를 가져온다
    typingTxt = [...typingTxt]; // 한글자씩 자른다.

    // 이모지 관련해서 이상한 공백 생길경우 배열에서 없애주기
    $(typingTxt).each(function(idx, val){
        if(val=='') {typingTxt.splice(idx, 1);}
    });

    if(typingBool==false){ // 타이핑이 진행되지 않았다면
        typingBool=true;
        var tyInt = setInterval(typing, 90); // 반복동작
    }

    function typing(){
        if(typingIdx<typingTxt.length){ // 타이핑될 텍스트 길이만큼 반복
            $(".typing").append(typingTxt[typingIdx]); // 한글자씩 이어준다.
            typingIdx++;
        } else{
            clearInterval(tyInt); //끝나면 반복종료
        }
    }
    // return;
    setTimeout(function(){
        $(".pageCover").removeClass("blur");
        if($("#pop_rsvp").hasClass("needShow")) {
            $("#pop_rsvp").css("display", "block");
        }
        $(".splash").addClass("animate__animated animate__fadeOut");
        setTimeout(function(){

            if(isBgm) { bgmAniFunc(); bgmStreaming(); }

            $(".splash").detach();

            if(isGarland) { floatGarland(); };
            onScroll()

            //========================================
            //========================================
            //========================================
            /*$(".floatingBox").addClass("h animated animate__fadeInUp");
            setTimeout(function(){
                $(".floatingBox").toggleClass("hi");
            }, 2000);*/
            //========================================
            //========================================
            //========================================

        }, 1000);
    }, 2200);
}

// 오프닝 V2
function splash_v2(isBgm, isGarland) {

    offSplash();
    const v2 = document.querySelector(".ltt_wrapper.v2");
    if(v2) {
        v2.style.display = 'block';
    }

    const splashElement = document.querySelector('#splash_v2_id');
    splashElement.style.background = "transparent";
    splashElement.classList.remove('keys');
    void splashElement.offsetWidth; // 강제 리플로우 발생

    G_ANI_LTT_OBJ = lottie.loadAnimation({
        container: document.getElementById('opening-v2-text'),
        renderer: 'svg',
        loop: false,
        autoplay: false,
        path: "/src/bodymovin/v2.json"
    });

    // DOMLoaded 이벤트 리스너를 별도로 정의
    function onDOMLoaded() {
        G_ANI_LTT_OBJ.goToAndStop(0, true);
        G_ANI_LTT_OBJ.play();
        splashElement.classList.add("keys");
    }

    // complete 이벤트 리스너를 별도로 정의
    function onAnimationComplete() {

        // 새 animationend 이벤트 리스너 추가
        function onAnimationEnd() {

            splashElement.style.display = "none";
            splashElement.removeEventListener('animationend', onAnimationEnd);  //console.log("제거");

            if (isBgm) {
                bgmAniFunc();
                bgmStreaming();
            }
            if (isGarland) {
                floatGarland();
            }
            if($("#pop_rsvp").hasClass("needShow")) {
                $("#pop_rsvp").css("display", "block");
            }
            onScroll()
        }
        // 이전 animationend 이벤트 리스너 제거
        splashElement.removeEventListener('animationend', onAnimationEnd);  //console.log("제거");
        splashElement.addEventListener('animationend', onAnimationEnd);  //console.log("등록");
    }

    // 이벤트 리스너 등록
    G_ANI_LTT_OBJ.addEventListener('DOMLoaded', onDOMLoaded);
    G_ANI_LTT_OBJ.addEventListener('complete', onAnimationComplete);

}

// 오프닝 V3
function splash_v3(isBgm, isGarland) {

    offSplash();
    const v3 = document.querySelector(".ltt_wrapper.v3");
    if(v3) {
        v3.style.display = 'block';
    }

    const splashElement = document.querySelector('#splash_v3_id');
    splashElement.classList.remove('keys');
    void splashElement.offsetWidth; // 강제 리플로우 발생

    // 애니메이션 JSON 파일을 먼저 로드
    fetch('/src/bodymovin/v3.json')
        .then(response => response.json())
        .then(animationData => {

            // 모든 레이어의 스트로크 색상을 하얀색으로 변경
            animationData.layers.forEach(layer => {
                if (layer.shapes) {
                    layer.shapes.forEach(shape => {
                        // shape의 각 항목에서 stroke('st') 속성을 찾음
                        findAndChangeStrokeColor(shape);
                    });
                }
            });

            // 수정된 JSON 데이터를 사용하여 애니메이션 로드
            G_ANI_LTT_OBJ = lottie.loadAnimation({
                container: document.getElementById('opening_v3'), // 애니메이션이 들어갈 div
                renderer: 'svg',
                loop: false,
                autoplay: false, // 자동 재생 활성화
                animationData: animationData // 수정된 JSON 데이터를 사용
            });

            // DOMLoaded 이벤트 리스너를 별도로 정의
            function onDOMLoaded() {
                G_ANI_LTT_OBJ.goToAndStop(0, true);
                G_ANI_LTT_OBJ.play();
                splashElement.classList.add("keys");
            }

            // complete 이벤트 리스너 정의 및 등록
            function onAnimationComplete() {

                function onAnimationEnd() {

                    splashElement.style.display = "none";
                    splashElement.removeEventListener('animationend', onAnimationEnd); //console.log("제거");

                    if (isBgm) {
                        bgmAniFunc();
                        bgmStreaming();
                    }
                    if (isGarland) {
                        floatGarland();
                    }
                }
                splashElement.removeEventListener('animationend', onAnimationEnd); //console.log("제거");
                splashElement.addEventListener('animationend', onAnimationEnd); //console.log("등록");
            }

            // 이벤트 리스너 등록
            G_ANI_LTT_OBJ.addEventListener('DOMLoaded', onDOMLoaded);
            G_ANI_LTT_OBJ.addEventListener('complete', onAnimationComplete);

        })
        .catch(error => console.error('Error loading the animation:', error));

    // 재귀적으로 모든 객체 내의 'st' 속성을 찾아 색상 변경
    function findAndChangeStrokeColor(shape) {
        if (shape.ty === 'st') { // 'st'는 stroke를 의미
            shape.c.k = [1, 1, 1, 1]; // RGB [1, 1, 1] = 하얀색
        } else if (shape.it) {
            shape.it.forEach(subShape => {
                findAndChangeStrokeColor(subShape); // 하위 객체에서 재귀적으로 탐색
            });
        }
    }
}





