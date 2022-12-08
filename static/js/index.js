let refresh = 0
let post_id
let text_input
let confirm_button_id
let date = getFormatDate(new Date())
$('#post_button').click(function(e){
    let post_area = $('#post_area').val()
    $.ajax({
        type: 'POST',
        url: '/api/posts',
        data: {'post_give': post_area,'date_give': date},
        success: function(response){
            window.location.reload()
        },
        error: function(response){

        }
    })
})
$('#modify_button').click(function(){
    post_id = $('#modify_button').attr('name')
    text_input = $('#'+post_id)
    text_input.attr('readonly', false)
    text_input.focus()
    confirm_button_id = '#confirm_button'+post_id
    $('#confirm_button'+post_id).attr('hidden', false)
})
function modify_check(){
    $.ajax({
        type: 'PUT',
        url: '/api/posts',
        data: {'id_give': post_id, 'post_give': text_input.val(),'date_give': date},
        success: function(response){
        if (response['msg']=='success'){
            refresh = 1
            modalOpen('글 수정 완료!')
        }
        },
        error: function(response){

        }
    })
}
$('#search_input').keyup(function(e){
    if(e.keyCode == 13){
        $('#search_form').submit()
    }
})
$(document).on('click', '#reply_toggle', function(){
    let id = $(this).attr('class')
    let modal = $('.reply_container'+id)
    if(modal.attr('style') == 'display:none'){
        modal.attr('style', 'display:block')
    } else{
        modal.attr('style', 'display:none')
    }
})
$('#reply_button').click(function(){
    let id = $(this).attr('name')
    let reply_text = $('#reply_text'+id).val()
    if(reply_text == ''){
        modalOpen("글을 입력하세요!")
    }
    $.ajax({
        type: 'POST',
        url: '/api/replies',
        data: {'id_give': id, 'reply_give': reply_text, 'date_give': date},
        success: function(response){
            if(response['msg'] == 'success'){
                let append_reply = `<div class="user-profile">
                                        <img src="../static/images/user.png">
                                    <div>
                                        <p>아이디</p>
                                        <span>날짜</span>
                                    </div>
                                        <input type="text" id="reply_content_box" value="${reply_text}" class="form-control" style="display: inline-block" readonly value="답글입니다"/>
                                    </div>
                `
                $('.reply_container'+id).prepend(append_reply)
            }
        },
        error: function(response){

        }
    })
})
$('#form_image').change(function(e) {
    let file = e.target.files
    preview(file[0], '.image_input_box')
})



$(document).on('click','#delete_button', function(){
    post_id=$(this). attr('name')
    $.ajax({
        type: 'DELETE',
        url: '/api/posts',
        data: {'post_give': post_id},
        success: function (result) {
            if (result['msg'] == 'deleted') {
               refresh=1
                modalOpen("deleted")
            }
        },
        error: function (response) {

        }
    })
}
)
