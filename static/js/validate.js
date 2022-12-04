function check_id(user_id, url){
    if(user_id === ''){
        modalOpen('아이디 칸이 비어있습니다.')
        return
    }
    $.ajax({
        type : "POST",
        url : url,
        data : {'id_give': user_id},
        success : function (response){
            if(user_id == response['msg']){
                modalOpen("중복된 아이디가 있습니다.")
                return
            } else{
                id_check = true
                modalOpen("중복된 아이디가 없습니다.")
            }
        }
    })
}

