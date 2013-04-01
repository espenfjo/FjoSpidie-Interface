var failed = false;
var blocked = false;

$(document).ready(function(){
    $("#urlform").submit(
        function(){
            console.info("Posting");
            event.preventDefault();
            
            var $form = $( this );
            term = $form.find( 'input[name="s"]' ).val();
            url = $form.attr( 'action' );
            $.ajax({
                type: "POST",
                url: url,
                data: $("#urlform").serialize(),
                async: false,
                success: function(response) { 
                    console.info("Posted" );
                    console.info("uuid: " + response.uuid);
                    
                    window.location.href =  "/report/"  + response.uuid;                    
                },
                error: function(){
                    console.info("fuck off");                    
                }
            });
        });
});


$(document).ready(function(){
    $("#login").submit(
        function(){
            return login();
        });
});

$(document).ready(function() {
    $("th.hheader").click( function() { showAll() } );
    
    var lol = 0;
    
    $.ajaxSetup({
        timeout: 1,
        retryAfter: 2000
    });
    
    
    if( $("#report").length > 0) {        
        checkIfFinished();
    }
    
    $(".fancybox-thumb").fancybox({
        prevEffect: 'none',
        nextEffect: 'none',
        scrolling: 'true',
        helpers: {
            title: {
                type: 'outside'
            },
            thumbs: {
                width: 50,
                height: 50
            }
        }
    });
    
   
    var active;
    $("div.headers").hide();
    
    
    $("tr.connection").click(function () {
        var data = $(this).find("div.headers");
        console.info(data);
        if (!data.is(active) && typeof active !== 'undefined') {
            active.hide();
        }
        data.toggle();
        active = data;
    });
});


function showAll(){
    $("tr.connection").each( function( index ) {
        var data = $(this).find("div.headers");
        data.toggle();
    } );
}

function checkIfFinished(){
        $.ajax({
            url: window.location.href,
            type: 'GET',
            async: false,
            cache: false,
            contentType: 'application/json',
            success:function(){
                console.info("Success");
                if (failed === true){
                    failed = false;
                    window.document.location.reload(true);
                }                    
                $.unblockUI();
            },            
            error: function(data, textStatus){
                if(blocked === false){
                    $.blockUI({ message: '<h1><img src="/static/images/busy.gif" /> Running FjoSpidie...</h1>' });
                    blocked = true;
                }
                failed = true;
                console.info("Failed: " + textStatus );
                setTimeout(checkIfFinished, 2000);
            }
        });
}



function hideAllMessages()
{
    var messagesHeights;
    
    messagesHeights = $('.error').outerHeight(); // fill array
    $('.error').css('top', -messagesHeights); //move element outside viewport
}
function showMessage(type)
{
    var data  = $("p#errormsg").text();
    if ( data ){
        hideAllMessages();
        $('.container').animate({"top": "+=80px"});
        $('.error').animate({top:"0"}, 500);
    }
}

$(document).ready(function(){

    // Initially, hide them all
    hideAllMessages();
    
    // Show message
    showMessage();

     // When message is clicked, hide it
    $('.error').click(function(){
        $(this).animate({top: -$(this).outerHeight()}, 500);
        $('.container').animate({"top":"-=80px"}, 500);

    });

});


$(document).ready(function(){
    $('tr.report').click(function(){
        $.blockUI({ message: '<h2><img src="/static/images/busy.gif" /> Loading report...</h2>' }); 
        window.location.assign( $(this).find('td').attr('rel') );
//        document.location.href = $(this).find('td').attr('rel');
    });
});
