$('.page-item').on("click", function(e){
    let current_page = e.target.innerHTML       // 현재 클릭한 페이지
    let url = "/page/profile/post?page=" + current_page
    location.href = url
})