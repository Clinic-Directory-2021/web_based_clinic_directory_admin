$('.right').hide();

clinic_id = "";
image_directory = "";

function showClinicInfo(clinic_address, clinic_contact_number, clinic_description,clinic_img_directory,clinic_img_url,clinic_name,opening_time,closing_time,email,latitude,longitude,total_items,user_id ){
    $(".available-items").remove();


    $('.right').show();

    $("#showClinicImg").attr("src", clinic_img_url);
   
    $('#showClinicName').html(clinic_name);

    $('#showClinicAddress').html(clinic_address);
    
    $('#showClinicName').html(clinic_name);
    
    $('#showClinicTime').html(opening_time + ' - ' + closing_time);

    $('#showClinicNumber').html(clinic_contact_number);
    
    $('#showClinicDescription').html(clinic_description);

    $('#loading').show();

    clinic_id = user_id;
    image_directory = clinic_img_directory

    $.post({
        type: 'post',
        url: "/clinic/",
        data: {
            user_id_post: user_id,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function(data){
            

        },
        error: function(data){
            $('#loader').hide();
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                      })
        },

    })
    .done(function(data){
        //console.log(data);
        $('#loading').hide();
        $( ".available-items" ).remove();
        $('.info-body').append(data);
    });



}



function deleteClinic(){
    Swal.fire({
        icon: 'question',
        title: 'Do you Really Want to Delete this Clinic?',
        text: 'This Cannot Be Undone!',
        showDenyButton: true,
        showCancelButton: true,
        showConfirmButton: false,
        denyButtonText: `Delete`,
      }).then((result) => {
          if (result.isDenied) {
            var url = "/deleteClinic";

            // Construct the full URL with "id"
            document.location.href = url + "?clinic_id=" + clinic_id+ "&image_directory=" + image_directory;
        }
      })

}