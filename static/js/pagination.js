$('.page-item').on("click", function(e){
    let current_page = e.target.innerHTML       // 현재 클릭한 페이지
    if(current_page == '»'){
        current_page += 1
    } else if(current_page == '«'){
        current_page == 1 ? current_page = 1 : current_page -= 1
    }
    let url = "/page/profile/post?page=" + current_page
    location.href = url
})