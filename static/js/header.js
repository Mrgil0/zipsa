function menuOnOff(){

	if($("#MenuWrap").attr("class").indexOf("Off") > -1){

		this.menuOn();

	}else{

		this.menuOff();

	}

}

function menuOn(){

	$("#MenuWrap").removeClass("menuOff");

	$("#MenuWrap").addClass("menuOn");

}

function menuOff(){

	$("#MenuWrap").removeClass("menuOn");

	$("#MenuWrap").addClass("menuOff");

	$("#Container").css('left','0px');

}