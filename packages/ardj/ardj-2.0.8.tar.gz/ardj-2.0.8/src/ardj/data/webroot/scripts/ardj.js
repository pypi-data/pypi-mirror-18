/**
 * Simplifies substring replacement.  Usage:
 * alert("{a}, {b}!".format({a: "hello", b: "world"}));
 */
function fmt(s, args)
{
    var formatted = s;
    for (arg in args) {
        var repeat = true;
        while (repeat) {
            var tmp = formatted.replace("{" + arg + "}", args[arg]);
            if (tmp == formatted)
                repeat = false;
            else
                formatted = tmp;
        }
    }
    return formatted;
};

jQuery(function ($) {
    $(document).on("click", "button.trigger", function (e) {
        e.preventDefault();
        $(this).blur();
        $(document).trigger($(this).attr("data-trigger"));
    });

    $(document).on("click", ".hometabs a", function (e) {
        e.preventDefault();
        $(this).blur();

        var tab_id = $(this).attr("href").substr(1);
        $(".tab").hide();
        $("#" + tab_id + "_tab").show();

        $(this).closest("ul").find("li").removeClass("active");
        $(this).closest("li").addClass("active");
    });

    $(document).on("ardj.home.refresh", function (e) {
        $.ajax({
            url: "/",
            type: "GET",
            dataType: "html"
        }).done(function (res) {
            $("#queue_tab").html($(res).find("#queue_tab").html());
            $("#recent_tab").html($(res).find("#recent_tab").html());
        });
    });
});

/**
 * Custom audio player.
 **/
jQuery(function ($) {
    $(".player[data-stream]").each(function () {
        var ctl = $(this);
        var playing = false;
        var stream = ctl.attr("data-stream");

        $(this).html("<button class='btn btn-default trigger' data-trigger='ardj.home.refresh'><i class='glyphicon glyphicon-refresh'></i></button><button class='btn btn-small btn-primary play'>Play</button><button class='btn btn-small btn-primary stop' style='display:none'>Stop</button><a class='btn btn-small btn-default async post' href='/skip'>Skip</a><span class='nowplaying'></span>");

        $(this).find(".play").on("click", function (e) {
            e.preventDefault();
            $(this).hide();
            ctl.append("<audio autoplay='autoplay' preload='none' style='display:none'><source type='audio/mpeg' src='" + stream + "?random=" + Math.random() + "'/></audio>");
            ctl.find(".stop").show();
            playing = true;
        });

        $(this).on("click", ".stop", function (e) {
            e.preventDefault();
            $(this).hide();
            ctl.find("audio").remove();
            ctl.find(".play").show();
            playing = false;
        });

        // Open links in new tab when playing
        $(document).on("click", "a", function (e) {
            if (!playing)
                return;
            if ($(this).is(".async"))
                return;

            var href = $(this).attr("href");
            if (href.substr(0, 1) == "#")
                return;

            e.preventDefault();
            window.open(href, "_blank");
        });
    });
});


/**
 * Now playing.
 ***/
jQuery(function ($) {
    var last = null;

    var update = function () {
        var url = "/status.json";
        if (last)
            url += "?last=" + last;

        $.ajax({
            url: url,
            type: "GET",
            dataType: "json"
        }).done(function (res) {
            res = $.extend({
                id: null,
                artist: null,
                title: null
            }, res);

            if (last && last != res.id)
                $(document).trigger("ardj.home.refresh");

            last = res.id;

            var message = fmt("Current: {artist} -- <a href='/track/{id}' target='_blank'>{title}</a>", {
                artist: res.artist,
                title: res.title,
                id: res.id
            });

            $(".nowplaying").html(message);
        }).always(function () {
            setTimeout(update, 1000);
        });
    };

    setTimeout(update, 1000);
});


/**
 * Replacement alert.
 *
 * Replace the built in alert function with an html message box, if there is one.
 **/
jQuery(function ($) {
    $("#msgbox:first").each(function (e) {
        var box = $(this);
        box.hide();

        var timer = null;

        window.alert = function (msg) {
            if (timer !== null) {
                clearTimeout(timer);
                timer = null;
            }

            box.html(msg);
            box.show();

            timer = setTimeout(function () {
                box.hide("slow");
            }, 5000);
        };

    });
});

// vim: set ts=4 sts=4 sw=4 et:
