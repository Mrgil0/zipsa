let pw_check = false
$('.nav-item a').on("click", function(){
    $('.nav-item a').removeClass("active")
    $(this).removeClass("link-dark")
    $(this).addClass("active")
})

$("#password_chk_button").click(function(){
    let password = $('#chk_input').val()
    check_pw(password, '/api/checkpw', '비밀번호')
})