var $headers = $('.header').click(function () {
    $(this).find('span').text(function (_, value) {
        return value == '-' ? '+' : '-'
    });
    $(this).nextUntil('tr.header').slideToggle(100, function () {});
});