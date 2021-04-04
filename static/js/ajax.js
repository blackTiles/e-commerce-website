$(document).ready(function() {

	$('#formProfile').on('submit', function(event) {

		$.ajax({
			data : {
				user_name : $('#p_username').val(),
				user_email : $('#p_email').val()
			},
			type : 'POST',
			url : '/update_profile'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {       
				$('#successAlert').text(data.success).show();
				$('#errorAlert').hide();
                $('#_user_id').text(data.username);
			}

		});

		event.preventDefault();

	});

	$('#formProfile').on('submit', function(event) {

		$.ajax({
			data : {
				user_name : $('#p_username').val(),
				user_email : $('#p_email').val()
			},
			type : 'POST',
			url : '/update_profile'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {       
				$('#successAlert').text(data.success).show();
				$('#errorAlert').hide();
                $('#_user_id').text(''+data.username);
			}

		});

		event.preventDefault();

	});

	

});

