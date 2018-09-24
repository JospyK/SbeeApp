$(function (){
	$('#markasread').click(function (){
		notificationCount = $('.label-warning.count').text();
		if(notificationCount !== 0){	
			markNotificationAsRead(notificationCount);
		}
	})
})

function markNotificationAsRead(notificationCount){
	$.get('/dashboard/markasread');
}