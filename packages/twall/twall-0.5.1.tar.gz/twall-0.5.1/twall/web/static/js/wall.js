$(document).ready(function (e) {
    $('.search-panel .dropdown-menu').find('a').click(function (e) {
        e.preventDefault();
        var param = $(this).attr("href").replace("#", "");
        var mode = $(this).text();
        $('.search-panel span#search-mode').text(mode);
        $('.input-group #search-param').val(param);
    });

    $('#search').click(function (e) {
        performSearch()
    });

    $('#search-field').keydown(function (e) {
        if (e.keyCode == 13) {
            performSearch()
        }
    });

    function performSearch() {
        var query = $('#search-field').val();
        var mode = $('#search-param').val();
        var currentLocation = [location.protocol, '//', location.host, location.pathname].join('');
        window.location = currentLocation + '?q=' + encodeURIComponent(query) + '&mode=' + mode;
    }
});