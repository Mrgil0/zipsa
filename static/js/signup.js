let refresh = 0
let id_check = false
let file_url
function join(){
    let user_id = $('#join_user_id').val()
    let password = $('#join_password').val()
    let password_chk = $('#join_password_chk').val()
    let email = $('#join_email').val()
    let pet_type = $('#pet_type_form').val()
    let pet_name = $('#pet_name').val()
    let pet_introduce = $('#pet_introduce').val()
    if([user_id, password, email, pet_type, pet_name, pet_introduce].includes('')){
        modalOpen('칸이 비어있습니다.')
        return
    }
    if(password != password_chk){
        modalOpen('비밀번호가 일치하지 않습니다.')
        return
    }
    if(!id_check){
        modalOpen('아이디 중복체크가 필요합니다.')
        return
    }
    $.ajax({
        type : "POST",
        url : "/api/user/signup",
        data : {'id_give': user_id, 'pw_give': password, 'em_give': email,
            'pet_type_give': pet_type, 'pet_name_give': pet_name, 'pet_introduce_give': pet_introduce,'pet_image_src': file_url},
        success : function (response){
            let result = response['msg']
            if(result === 'success'){
                refresh = 1
                modalOpen('회원가입 완료')
                id_check = false
            }
        }
    })
}
$(document).on('click', '#user_id_check_btn', function(){
    let user_id = $('#join_user_id').val()
    check_id(user_id, '/api/checkid', "아이디")
})
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