$().ready(function(){
    $('#btnSend').click(function(){
         $.ajax({
             type: 'POST',
             url: '/pdf',
             data: $('#export').get(0).outerHTML,//.html(),
             dataType: 'html',
             success: function(ret){
                  if (ret == 'OK'){

                    //var notice = new PNotify({
                    $.pnotify({
                        title: 'Notification',
                        text: 'PDF is generated successfully!',
                        type: 'success',
                        icon: 'ui-icon ui-icon-check'

                    });
                    //notice.get().click(function() {
                    //    notice.remove();
                    //});
                  }
                  else{
                    //new PNotify({
                    $.pnotify({
                                title: 'Notification',
                                text: 'Some error occurred during PDF generation!',
                                type: 'error',
                                icon: 'ui-icon ui-icon-check'

                    });
                  }

            } 
        }); 
    });
});
