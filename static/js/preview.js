function preview(f, div) {
    let filename = f.name
    if (filename.length > 10) {
        filename = filename.substring(0, 7) + "...";
    }
    //div에 이미지 추가
    let img_div = '<div style="display: inline-flex; padding: 10px;"  class="picdiv">';

    //이미지 파일 미리보기
    if (f.type.match('image.*')) {
        let reader = new FileReader(); //파일을 읽기 위한 FileReader객체 생성
        reader.onload = function (e) { //파일 읽어들이기를 성공했을때 호출되는 이벤트 핸들러
            img_div += '<img src="' + e.target.result + '" title="' + filename + '" width=100 height=100 />';
            $(img_div).prependTo('#image_input_box');
            file_src = e.target.result
        }
        reader.readAsDataURL(f);
    } else {
        img_div += '<img src="/resources/img/fileImg.png" title="' + filename + '" width=100 height=100 />';
        $(img_div).prependTo(div);
    }
    $('.picdiv').attr('src')
}