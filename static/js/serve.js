$().ready(function(){
    $('#btnSend').click(function(){
         $.ajax({
             type: 'POST',
             url: '/pdf',
             data: $('#export').get(0).outerHTML,//.html(),
             dataType: 'html',
             success: function(data){
                    window.open('/showpdf/'+data, '_blank');
                    $.pnotify({
                        title: 'Notification',
                        text: 'PDF is generated successfully!',
                        type: 'success',
                        icon: 'ui-icon ui-icon-check'
                    });
             },
             error: function(){
                    $.pnotify({
                        title: 'Notification',
                        text: 'Some error occurred during PDF generation!',
                        type: 'error',
                        icon: 'ui-icon ui-icon-check'
                    });
             }
        });
    });
    $('#premier').click(function(){
        $.ajax({
            url: '/premier',
            method: 'GET',
            dataType: 'html'
        }).success(function(data){
            document.write(data);
            document.close();
        });
    });

    $('#invoice').click(function(){
        $.ajax({
            url: '/invoice',
            method: 'GET',
            dataType: 'html'
        }).success(function(data){
            document.write(data);
            document.close();
        });
    });
});
