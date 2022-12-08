$(document).on('click', '#closeBtn', function(){
    $("#modal").css('display', 'none')
})

$(document).on('click', '#modalClose', function(){
    $("#modal").css('display', 'none')
})

function modalOpen(str){
    let scrollTop = document.scrollingElement.scrollTop
    let windowHeight = window.innerHeight
    $('#modal').css('display', 'flex')
    $('#modal.modal-overlay').css('width', document.documentElement.scrollWidth)
    $('#modal.modal-overlay').css('height', windowHeight)   //창높이만큼 세로 설정
    $('#modal.modal-overlay').css('top', scrollTop )        //내가 올린 스크롤만큼 밑으로 이동
    $('#context').html(str)
}

$("#modal").click(function(e){
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) { //클릭한 곳이 모달창 바깥 영역(modal-overlay)이면 꺼짐
        this.style.display = "none"
    }
})

$(document).keyup(function(e){
    const modal = $('#modal').css('display')
    if(modal === "flex" && e.key === "Escape") {    //모달창이 켜진 상태에서 esc를 누르면 꺼짐
        $("#modal").css('display', 'none')
    }
})

$("#modalClose").click(function(){
    $('#modal').css('display', 'none')
    $('#modal').css('left', '0')
    $('#modal').css('top', '0')
    if(refresh == 1){
        refresh = 0
        location.reload()
    }
})
