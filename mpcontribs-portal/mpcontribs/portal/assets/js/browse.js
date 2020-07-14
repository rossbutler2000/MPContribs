$(document).ready(function () {
    var imageNames = require.context('../images/', false, /\.(png)$/).keys();

    $.each(imageNames, function(idx, name) {
        var imageName = name.replace('./', '');
        import('../images/' + imageName).then(function(src) {
            var suffix = imageName.replace('.png', '_img');
            $('[name=thumbnail_' + suffix + ']').each(function(idx) {
                var img = $("<img/>", {src: src.default, width: "100%"});
                $(this).append(img);
            });
        }).catch(function(err) { console.log(err); });
    });

    $('[name=thumbnail]').on('click', function(e) {
        e.preventDefault();
        var selector = '#' + $(this).attr("id") + "_modal";
        $(selector).addClass("is-active");
        $("html").addClass("is-clipped");
    });

    $('[name=thumbnail_close]').on('click', function(e) {
        e.preventDefault();
        window.scrollTo(0, 0);
        $(this).parent().removeClass("is-active");
        $('html').removeClass("is-clipped");
    });
});
