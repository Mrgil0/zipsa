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
        url : "/api/users/signup",
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
    element.addEventListener("click", e=>{  // changed 모든 요소의 클릭이벤트
        let type_text = e.target.innerHTML               // 클릭한 타켓의 값
        let pet_type = $('#pet_type_form')
        if(type_text === '직접 입력하기'){
            pet_type.attr('readonly', false)
            pet_type.val('')
            pet_type.attr('placeholder', '입력하세요')
            pet_type.focus()
        } else{
            pet_type.attr('readonly', true)
            pet_type.val(type_text)
        }

    })
})
 $('#choose_image').change(function(e){
    let file =  e.target.files[0]
     file_url = window.URL.createObjectURL(file)
    preview(file, '#image_input_box')
})


$(function(){
    $('#join_password').keyup(function(){
      $('#chkNotice').html('');
    });

    $('#join_password_chk').keyup(function(){
        if($('#join_password').val() != $('#join_password_chk').val()){
          $('#chkNotice').html('비밀번호 일치하지 않음');
          $('#chkNotice').attr('color', '#f82a2aa3');
        } else{
          $('#chkNotice').html('비밀번호 일치함');
          $('#chkNotice').attr('color', '#199894b3');
        }

    });
});