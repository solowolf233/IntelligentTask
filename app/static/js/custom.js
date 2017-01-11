/*
Theme: eLearning - Free Educational Responsive Web Template
Description: Free to use for personal and commercial use
Author: WebThemez.com
Website: http://webthemez.com
Note: Please do not remove the footer backlink (webthemez.com)--(if you want to remove contact: webthemez@gmail.com)
Licence: Creative Commons Attribution 3.0** - http://creativecommons.org/licenses/by/3.0/
*/
$(function(){
	
	var nav=$(".navbar-wrapper");
	var win=$(window);
	var sc=$(document);
	win.scroll(function(){
		if(sc.scrollTop()>=10){
			nav.addClass("fixednav"); 
			$(".topBtn").fadeIn();
		}else{
			nav.removeClass("fixednav");
			$(".topBtn").fadeOut();
		}
	});
	
	$('a.topBtn').click(function(){ 
		$('html, body').animate({scrollTop:0}, 'slow'); 
		return false; 
	});
	


});