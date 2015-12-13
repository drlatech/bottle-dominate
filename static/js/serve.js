$().ready(function(){
    $('#btnSend').click(function(){
         $.ajax({
             type: 'POST',
             url: '/pdf',
             data: $('#export').html(),
             dataType: 'text',
             success: function(ret){
                  if (ret == 'OK'){

                    var notice = new PNotify({
                        title: 'Notification',
                        text: 'PDF is generated successfully!',
                        type: 'success',
                        buttons: {
                            closer: false,
                            sticker: false
                        }
                    });
                    notice.get().click(function() {
                        notice.remove();
                    });
                  }
                  else{
                    new PNotify({
                                title: 'Notification',
                                text: 'Some error occurred during PDF generation!',
                                type: 'error'
                    });                  }

            } 
        }); 
    });
});
