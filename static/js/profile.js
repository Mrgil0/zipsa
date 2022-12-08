$('.nav-item a').on("click", function(){
    $('.nav-item a').removeClass("active")
    $(this).removeClass("link-dark")
    $(this).addClass("active")
})

$("#password_chk_button").click(function(){
    let password = $('#chk_input').val()
    check_pw(password, '/api/checkpw', '비밀번호')
})
let file_url
function modify_user(){
    let password = $('#modify_password').val()
    let password_chk = $('#modify_password_chk').val()
    let email = $('#modify_email').val()
    let pet_type = $('#pet_type_form').val()
    let pet_name = $('#modify_pet_name').val()
    let pet_introduce = $('#modify_pet_introduce').val()
    if([password, password_chk, email, pet_type, pet_name, pet_introduce].includes('')){
        modalOpen('칸이 비어있습니다.')
        return
    }
    if(password !== password_chk){
        modalOpen('비밀번호가 일치하지 않습니다.')
        return
    }
    $.ajax({
        type : "PUT",
        url : "/api/user/modify",
        data : {'pw_give': password, 'em_give': email,
            'pet_type_give': pet_type, 'pet_name_give': pet_name, 'pet_introduce_give': pet_introduce,'pet_image_src': file_url},
        success : function (response){
            let result = response['msg']
            if(result === 'success'){
                refresh = 1
                modalOpen('회원정보 수정 완료')
            }
        }
    })
}
let changed = document.querySelectorAll(".dropdown-item")
changed.forEach(element=>{
    element.addEventListener("click", e=>{
        let pet_name = e.target.innerHTML
        let pet_type = $('#pet_type_form')
        if(pet_name === '직접 입력하기'){
            pet_type.attr('readonly', false)
            pet_type.val('')
            pet_type.attr('placeholder', '입력하세요')
            pet_type.focus()
        } else{
            pet_type.attr('readonly', true)
            pet_type.val(pet_name)
        }

    })
})
 $('#choose_image').change(function(e){
    let file =  e.target.files[0]
    if(file == null){
        file_url = 'no image'
    } else{
        file_url = window.URL.createObjectURL(file)
        $('#pet_image').attr('src', file_url)

    }
})