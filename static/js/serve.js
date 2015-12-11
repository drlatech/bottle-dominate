$(document).ready(function(){  
    $('#btnSend').click(function(){
         $.ajax({
             type: 'POST',
             url: '/pdf',
             success: function(data){
                  alert(data); 
            } 
        }); 
    });
});
