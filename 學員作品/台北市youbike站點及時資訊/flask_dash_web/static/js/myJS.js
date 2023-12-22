$(function(){
	
	var SS=$("#PIC li"),
		N=0,
		LL=SS.length;

	SS.eq(N).find("img").fadeIn();
	

	function GOGO(){
		
		var nextN=(N+1)%LL;
		
		SS.eq(N).find("img").fadeOut()
		SS.eq(nextN).find("img").fadeIn();
		N=nextN
		
	}
	
	setInterval(GOGO,3000)
	
})

