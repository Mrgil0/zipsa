function getFormatDate(date){
    let year = date.getFullYear();              //yyyy
    let month = (1 + date.getMonth());          //M
    month = month >= 10 ? month : '0' + month;  //month 두자리로 저장
    let day = date.getDate();                   //d
    let min = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
    day = day >= 10 ? day : '0' + day;          //day 두자리로 저장
    return  year + '-' + month + '-' + day + ' ' + min;       //'-' 추가하여 yyyy-mm-dd 형태 생성 가능
}