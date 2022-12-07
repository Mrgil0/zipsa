$('.page-item').on("click", function(e){
    let current_page = e.target.innerHTML
    if(current_page == '»'){
        current_page += 1
    } else if(current_page == '«'){
        current_page == 1 ? current_page = 1 : current_page -= 1
    }
    let url = "/page/profile/post?page=" + current_page
    location.href = url
})