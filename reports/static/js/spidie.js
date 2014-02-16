var failed = false;

var active;

var blocked = false;

$(document).ready(function() {
    setupListeners();
    $.ajaxSetup({
        timeout: 1,
        retryAfter: 2e3
    });
    if ($("#report").length > 0) {
        checkIfFinished();
    }
    $(".fancybox-thumb").fancybox({
        prevEffect: "none",
        nextEffect: "none",
        scrolling: "true",
        helpers: {
            title: {
                type: "outside"
            },
            thumbs: {
                width: 50,
                height: 50
            }
        }
    });
    $("div.headers").hide();
    hideAllMessages();
    showMessage();
    $('.alert').each(function(){
        var rel = $(this).attr('rel');
        $('#' + rel).addClass("suspicious alert alert-error");
    });
});

function setupListeners() {
    $("#submit-advanced").on("click", function() {
        $("#advanced-inputs").toggle();
        if ($("#advanced-inputs").is(":visible")) {
            $("#advanced-caret").removeClass("right-caret").addClass("caret");
        } else {
            $("#advanced-caret").addClass("right-caret").removeClass("caret");
        }
    });
    $("#submit-urlfdsa").on("click", function() {
        console.info("Posting");
        var form = $(this);
        term = form.find('input[name="s"]').val();
        url = "/job";
        var data = {
            useragent: $("#useragent").val(),
            ref: $("#referer").val(),
            url: $("#url").val()
        };
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            async: false,
            success: function(response) {
                window.location.href = "/report/" + response.uuid;
                console.info("Posted");
                console.info("uuid: " + response.uuid);
            },
            error: function() {
                console.info("Can not send JOB");
            }
        });
    });
    $("#login").submit(function() {
        return login();
    });
    $("th.hheader").click(function() {
        showAll();
    });
    $("tr.connection").click(function() {
        var data = $(this).find("div.headers");
        console.info(data);
        if (!data.is(active) && typeof active !== "undefined") {
            active.hide();
        }
        data.toggle();
        active = data;
    });
    $(".error").click(function() {
        $(this).animate({
            top: -$(this).outerHeight()
        }, 500);
        $(".container").animate({
            top: "-=80px"
        }, 500);
    });
    $("tr.report").click(function() {
        $.blockUI({
            message: '<h2><img src="/static/images/busy.gif" /> Loading report...</h2>'
        });
        window.location.assign($(this).find("td").attr("rel"));
    });

    $("tr.alert").click(function() {
        var aid = $(this).attr('rel');
        $('html, body').animate({ scrollTop: $('#' + aid ).offset().top -120 }, 'slow');
        $('#' + aid).click();

    });

    $(".signature").click(function() {
        var sid = $(this).attr('rel');
        $('html, body').animate({ scrollTop: $('#' + sid ).offset().top -120 }, 'slow');
        $('#' + sid).click();

    });

}

function showAll() {
    $("tr.connection").each(function(index) {
        var data = $(this).find("div.headers");
        data.toggle();
    });
}

function checkIfFinished() {
    $.ajax({
        url: window.location.href,
        type: "GET",
        async: false,
        cache: false,
        contentType: "application/json",
        success: function() {
            console.info("Success");
            if (failed === true) {
                failed = false;
                window.document.location.reload(true);
            }
            $.unblockUI();
        },
        error: function(data, textStatus) {
            if (blocked === false) {
                $.blockUI({
                    message: '<h1><img src="/static/images/busy.gif" /> Running FjoSpidie...</h1>'
                });
                blocked = true;
            }
            failed = true;
            console.info("Failed: " + textStatus);
            setTimeout(checkIfFinished, 2e3);
        }
    });
}

function hideAllMessages() {
    var messagesHeights;
    messagesHeights = $(".error").outerHeight();
    $(".error").css("top", -messagesHeights);
}

function showMessage(type) {
    var data = $("p#errormsg").text();
    if (data) {
        hideAllMessages();
        $(".container").animate({
            top: "+=80px"
        });
        $(".error").animate({
            top: "0"
        }, 500);
    }
}
