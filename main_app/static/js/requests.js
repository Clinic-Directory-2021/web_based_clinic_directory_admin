

function clinicAccept(clinic_address, clinic_contact_number, clinic_description,clinic_img_directory,clinic_img_url,clinic_name,opening_time,closing_time,email,latitude,longitude,total_items,user_id ){
    Swal.fire({
        title: 'Do you really want to Accept this Clinic?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Accept',
      }).then((result) => {
        if (result.isConfirmed) {
         
            $.ajax({
                type: 'post',
                url: "/acceptClinic/",
                data: {
                    clinicAddress: clinic_address,
                    clinicContactNumber: clinic_contact_number,
                    clinicDescription: clinic_description,
                    clinicImgDirectory: clinic_img_directory,
                    clinicImgUrl: clinic_img_url,
                    clinicName: clinic_name,
                    openingTime: opening_time,
                    closingTime: closing_time,
                    clinicEmail: email,
                    clinicLatitude: latitude,
                    clinicLongitude: longitude,
                    totalItems: total_items,
                    userId: user_id,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    },
                success: function(data){
                    $('#loader').hide();
                    location.reload();
                }, 
                error: function(data){
                    $('#loader').hide();
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                      })
                },
          
            });


        }
      })
}

function clinicDecline(user_id,clinic_img_directory, clinic_email ){
    Swal.fire({
        title: 'Do you really want to Decline this Clinic?',
        icon: 'question',
        showCancelButton: true,
        showDenyButton: true,
        showConfirmButton: false,
        denyButtonText: 'Decline',
      }).then((result) => {
        if (result.isDenied) {
         
            $.ajax({
                type: 'post',
                url: "/declineClinic/",
                data: {
                    userId: user_id,
                    clinicImgDirectory: clinic_img_directory,
                    clinicEmail: clinic_email,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    },
                success: function(data){
                    location.reload();
                    $('#loader').hide();
                }, 
                error: function(data){
                    $('#loader').hide();
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                      })
                },
          
            });


        }
      })
}