function redirectToAdmin(){
  window.location.replace("https://govet.herokuapp.com/login/");
}

$('#loginForm').on('submit', function(e){
    $('#loader').show();
    e.preventDefault();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/login_validation/",
        data: {
          login_email: $('#login_email').val(),
          login_password: $('#login_password').val(),
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          },
        success: function(data){
            $('#loader').hide();
            if(data=="Invalid Email or Password!"){
                //  $('#responseMessage').html(data);
                 Swal.fire({
                    icon: 'error',
                    title: data,
                    confirmButtonText: 'OKAY',
                  })
            }else if (data == 'Success!'){
                $('#loader').hide();
                Swal.fire({
                    position: 'middle',
                    icon: 'success',
                    title: 'Login Successful!',
                    showConfirmButton: true,
                    confirmButtonText: 'PROCEED',
                  }).then((result) => {
                    if (result.isConfirmed) {
                        location.reload();
                    }
                  })
            }
        },
        error: function(data){
            $('#loader').hide();
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
              })
        },
  
    });
  });