$(document).ready(function() {

    $('.addToCart').on('click', function(){
		var productId = $(this).attr('productId');
		req = $.ajax({
			url : '/addToCart',
			type : 'POST',
			data : {productId : productId}
		});
        req.done(function(data){
            $('#a'+productId).text(data.success);
            $('#a'+productId).css("background-color", "green");
        });
	});

    $('.dropItem').on('click', function(){
		var itemId = $(this).attr('item_id');
		req = $.ajax({
			url : '/dropFromCart',
			type : 'POST',
			data : {itemId : itemId}
		});
        req.done(function(data){
            $('#idItem'+itemId).css("display", "none");           
            $('#totalPrice').text('₹'+data.price);
            
        });
	});
    $('.cancelOrder').on('click', function(){
		var _orderID = $(this).attr('_orderID');
		req = $.ajax({
			url : '/cancelOrder',
			type : 'POST',
			data : {_orderID : _orderID}
		});
        req.done(function(data){
            $('#order_'+_orderID).css("display", "none");  
            
        });
	});
	$('#loginForm').on('submit', function(event){
		req = $.ajax({
			url : '/login',
			type : 'POST',
			data : {
				inputEmail : $('#inputEmail').val(),
				inputPass : $('#inputPassword').val()
			}
		});
        req.done(function(data){
            if(data.error){
				$('#alert-user').text(data.error);
			}
			else if(data.notExist){
				$('#alert-user').text(data.notExist);
			}
			else{
				location.reload();
			}
        });
		event.preventDefault();
	});
	$('#registerForm').on('submit', function(event){
		req = $.ajax({
			url : '/register',
			type : 'POST',
			data : {
				signUser : $('#sign_user').val(),
				signEmail : $('#sign_email').val(),
				signPass : $('#sign_pass').val()
			}
		});
        req.done(function(data){
            if(data.error){
				$('#alert-sign-user').text(data.error);
			}
			else if(data.alreadyExist){
				$('#alert-sign-user').text(data.alreadyExist);
			}
			else{
				window.location.href=data.verify;
			}
        });
		event.preventDefault();
	});
	$('#feedback').on('submit', function(event){
		req = $.ajax({
			url : '/feedback',
			type : 'POST',
			data : {
				sender_name : $('#sender_name').val(),
				sender_email : $('#sender_email').val(),
				sender_msg : $('#sender_msg').val()
			}
		});
        req.done(function(data){
            if(data.empty){
				$('#alert-feedback').text(data.empty);
			}
			else{
				$('#alert-feedback').text(data.sent);
			}
        });
		event.preventDefault();
	});
});