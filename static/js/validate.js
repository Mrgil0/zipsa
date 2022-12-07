function check_id(user_data, url, str){
    if(user_data === ''){
        modalOpen(str +' 칸이 비어있습니다.')
        return
    }
    $.ajax({
        type : "POST",
        url : url,
        data : {'data_give': user_data},
        success : function (response){
            if(user_data == response['msg']){
                modalOpen("중복된 " + str + "가 있습니다.")
                return
            } else{
                id_check = true
                modalOpen("중복된 " + str + "가 없습니다.")
            }
        }
    })
}
function check_pw(user_data, url, str){
    if(user_data === ''){
        modalOpen(str +' 칸이 비어있습니다.')
        return
    }
    $.ajax({
        type : "POST",
        url : url,
        data : {'data_give': user_data},
        success : function (response){
            if(response['msg'] == user_data){
                location.replace('/page/profile/user?result=true')
            } else{
                modalOpen(str + " 불일치")
            }
        }
    })
}

