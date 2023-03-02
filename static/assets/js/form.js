

function validateEmail(email){
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( email );
}

function contact()
{

    if($('#first_name').val()=='')
    {
        $('#first_nameStatus').show();          
        $('#first_nameStatus').html('First name are required.');

    }
    else
    {
        $('#first_nameStatus').html('');
    }
    if($('#email').val()=='')
    {
        $('#emailStatus').show();
        $('#emailStatus').html('Email id are required.');

    }
    else
    {

        $('#emailcheck').html('');

    }

    var email=$('#email').val();
    if(!validateEmail(email))
    {            
        $('#emailcheck').html('Enter a valid email id.');

    }
    else
    {

        $('#emailcheck').html('');

    }
    
    if($('#last_name').val()=='')
    {
        $('#last_nameStatus').show();
        $('#last_nameStatus').html('Last name are required.');

    }
    else
    {

     $('#last_nameStatus').html('');

 }
 if($('#message').val()=='')
 {
    $('#messageStatus').show();
    $('#messageStatus').html('Message are required.');

}
else
{

 $('#messageStatus').html('');

}
if($('#first_name').val()!='' && $('#email').val()!='' && $('#last_name').val()!='' && $('#message').val()!='' && validateEmail(email))
{   
    $('#formStatus').append("<div class='loader'></div>");
    $('.contactSave').hide();
    $.ajax({
        type : 'POST',
        url : '/',            
        data: $('#contactSave').serialize(),
        success: function(data) {

            if(data.type=='error')
            {

                $("#formStatus").addClass("formError");
                $("#formStatus").html(data.message);
            }  
            else
            {

                setTimeout(function(){
                    $("#formStatus").addClass("formSuccess");
                    $("#formStatus").html(data.message); 
                }, 2000);

                setTimeout(function(){                       
                    $("#formStatus").html('');                   
                    $('#first_name').val('');
                    $('#last_name').val('');
                    $('#email').val('');
                    $('#message').val('');                       
                }, 5000);

                setTimeout(function(){
                    $('.contactSave').show();
                    $('#formStatus .loader').removeClass("loader");
                }, 2000);

            }


        }

    }); 

}
else{
    return redirect('/')
}
} 
function signup()
{
    if($('#name').val()=='')
    {
        $('#nameStatus').show();
        $('#nameStatus').html('Please Enter The Full Name.');

    }          
    else
    {


        $('#nameStatus').html('');
    }
    if($('#email').val()=='')
    {        
        $('#emailStatus').show();    
        $('#emailStatus').html('Please Enter The Email Id.');

    }
    else
    {

        $('#emailStatus').html('');

    }
    var email=$('#email').val();
    if(!validateEmail(email))
    {            
        $('#validemailStatus').html('Enter a valid email id.');

    }
    else
    {

        $('#validemailStatus').html('');

    }

    if($('#number').val()=='')
    {        
        $('#numberStatus').show();    
        $('#numberStatus').html('Please Enter The Phone Number.');

    }
    else
    {

        $('#numberStatus').html('');

    }


    if($('#password').val()=='')
    {   $("#checkpasswordStatus").hide();
        $('#passwordStatus').show();
        $('#passwordStatus').html('Please Enter The Password.');

    }
    else 
    {
        $("#checkpasswordStatus").show();
     $('#passwordStatus').html('');

 }
 
 var password=$('#password').val();
 var pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
 if (pattern.test(password)){
        $("#checkpasswordStatus").html('');
        
    }
    else{
        $("#checkpasswordStatus").html('Minimum Length Of The Password is 8 with a mix of upper and lower case letters and numbers. and lower case letters, numbers and symbols');
    }




 if($('#confirmPassword').val()=='')
 {   $("#checkconfirmpasswordStatus").hide();
     $('#confirmpasswordStatus').show();
     $('#confirmpasswordStatus').html('Please Enter The Confirm Password.');

 }
 else 
 {
     $("#checkconfirmpasswordStatus").show();
  $('#confirmpasswordStatus').html('');

}


 if($('#confirmPassword').val()!='' && $('#password').val()!='' && $('#name').val()!='' && $('#email').val()!='' && $('#number').val()!='' && validateEmail(email) && pattern.test(password)==true )
 {
        // $('#formStatus').append("<div class='loader'></div>");
        // $('.signUp').hide(); 

        $.ajax({
            type : 'POST',
            url : '/sign-up',            
            data: $('#signUp').serialize(),
            success: function(data) {

                data=JSON.parse(data);
                if(data.type=='error')
                {
                 
                    $("#formStatus").addClass("fieldError");
                    $("#formStatus").html(data.message);
                   
                    
                }  
                else
                {
                    
                    $('#loaderStatus').append("<div class='loader'></div>");
                    // $('.signUp').hide(); 
                  

                    setTimeout(function(){
                        $("#formStatus").addClass("formSuccess");                      
                        $("#formStatus").html(data.message); 
                                            
                    }, 2000);

                   
                    
                    setTimeout(function(){      
                        $('#name').val('');
                        $('#email').val('');
                        $('#number').val('');
                        $('#password').val('');
                        $('#confirmPassword').val('');
                        $("#formStatus").html('');
                        // $("#show_login").html(data.return);
                        // window.location.href = "/sign-in";                                   
                    }, 4000);

                    setTimeout(function(){
                        // $('.signUp').show();
                        $('#loaderStatus .loader').removeClass("loader");
                    }, 2000);
                    

                }
            }
            

        }); 
    }

}

function signin()
{

 if($('#email').val()=='')
 {        
    $("#emailStatus").addClass("fieldError");
    $('#emailStatus').html('Please Enter The Email Id.');

}
else
{

    $('#emailStatus').html('');

}
var email=$('#email').val();
if(!validateEmail(email))
    {   
$("#validemailStatus").addClass("fieldError");        
$('#validemailStatus').html('Enter a valid email id.');


}
else
{

    $('#validemailStatus').html('');

}
if($('#password').val()=='')
{
   
    $('#passwordStatus').addClass("fieldError");
    $('#passwordStatus').html('Please Enter The Password.');
    $('#btn-submit-sign').show();

}
else
{

 $('#passwordStatus').html('');

}

if($('#confirmPassword').val()=='')
{
    
    $('#checkconfirmpasswordStatus').addClass("fieldError");
    $('#checkconfirmpasswordStatus').html('Please Enter The confirmPassword.');
    $('#btn-submit-sign').show();

}
else
{

 $('#checkconfirmpasswordStatus').html('');

}

if($('#password').val()!='' && $('#email').val()!='' && validateEmail(email))
{
    $('#btn-submit-sign').hide();

    $.ajax({
        type : 'POST',
        url : '/sign-in',            
        data: $('#signIn').serialize(),
        success: function(data) {


            if(data.type=='error')
            {
                $("#formStatus").addClass("fieldError");
                $("#formStatus").html(data.message);
                $('#btn-submit-sign').show();
                
            }  
            else
            {   

                $('#loaderStatus').append("<div class='loader'></div>");

                $('.btn-submit-sign').hide(); 

                 window.location.href="/dashboard";
               

            }
        }


    }); 
}

}



///start enquiry form js
$("input").on("keypress", function(e) {
    if (e.which === 32 && !this.value.length)
        e.preventDefault();
});


$( "#name" ).keyup(function() {
    $('#nameStatus').hide();
});

$( "#email" ).keyup(function() {
    $('#emailStatus').hide();
});

$( "#number" ).keyup(function() {
    $('#numberStatus').hide();
});

$( "#password" ).keyup(function() {
    $('#passwordStatus').hide();
});

  ///start sign up form js


  $( "#first_name" ).keyup(function() {
    $('#first_nameStatus').hide();
});
  $( "#last_name" ).keyup(function() {
    $('#last_nameStatus').hide();
});
  $( "#email" ).keyup(function() {
    $('#emailStatus').hide();
});
  $( "#message" ).keyup(function() {
    $('#messageStatus').hide();
});




  function passFunction() {

    var pass =  document.getElementById("password").value;   
    var conpass =  document.getElementById("confirmPassword").value;

    if(conpass==pass)
    {
        $("#confirmpasswordStatus").html('');
    }
    else{
        $("#confirmpasswordStatus").html('Password do not match');
    }
    
    
}

function myFunction() {

    var pass =  document.getElementById("password").value;   
    var conpass =  document.getElementById("confirmPassword").value;

    if(conpass==pass)
    {
        $("#confirmpasswordStatus").html('');
    }
    // else{
    //     $("#confirmpasswordStatus").html('Confirm Password do not match');
    // }
    
    
}



function forgetpassword()
{

    var email=$("#email").val();
    if(email==''){
        $("#emailStatus").addClass("fieldError");
        $('#emailStatus').html('Please Enter The Email Id.');  
        $('#forgetpasswordform').hide();

    }
    else
    {
        $("#emailvalidStatus").removeClass("fieldError");
        $('#emailvalidStatus').html('');
        $('#forgetpasswordform').show();
    }
    
    if(!validateEmail(email))
    {
        $("#emailvalidStatus").addClass("fieldError");
        $('#emailvalidStatus').html('Please Enter Valid Email Id.');
        $('#forgetpasswordform').hide();
    }
    else
    {
        $("#emailvalidStatus").removeClass("fieldError");
        $('#emailvalidStatus').html('');
        $('#forgetpasswordform').show();

    }

    

}