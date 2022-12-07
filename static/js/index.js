let refresh = 0
let post_id
let text_input
let confirm_button_id
$('#post_button').click(function(e){
    let post_area = $('#post_area').val()
    let date = getFormatDate(new Date())
    $.ajax({
        type: 'POST',
        url: '/api/posts',
        data: {'post_give': post_area,'date_give': date},
        success: function(response){
        if (response['msg']=='success'){
            modalOpen('글 작성 완료!')
        }
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
    let date = getFormatDate(new Date())
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