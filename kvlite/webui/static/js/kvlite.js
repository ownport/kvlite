$(document).ready( function() {
    get_collections();
});

function get_collections() {

    $.getJSON("/collections").done(function(json) {
        if (json.collections.length > 0) {
            $('#collections-list').empty();
            $.each(json.collections, function() {
                var collection = "<li><a class=\"collection-name\" role=\"menuitem\" tabindex=\"-1\" href=\"#\">"
                collection += this + "</a></li>"
                $("#collections-list").append(collection);
            });
            $(".collection-name").click(function(){
                var collection_name = this.text
                $("#current-collection").text(collection_name);
                get_data(collection_name)
            });
        };
    });

};

function get_data(collection_name) {

    $.getJSON("/collection/" + collection_name + "/").done(function(json) {
        if (json.status == "OK") {
            if (json.data.length > 0) {
                show_data_as_grid(json.data);
            } else {
                $("#collection-data").empty();
            };
        } else {
            console.debug(json)
        };
    });
};

function show_data_as_table(data) {

    $("#collection-data").empty();
    var content = "<table class=\"table table-stripped\">"
    content += "<tr> <th>Key</th> <th>Value</th> </tr>";
    $.each(data, function() {
        content += "<tr> <td>" + this[0] + "</td>";
        content += "<td>" + JSON.stringify(this[1]) + "</td> </tr>";
    });
    content += "</table>";
    $("#collection-data").append(content);
};

function show_data_as_grid(data) {

    $("#collection-data").empty();
    var content = "<div class=\"row\">"
    content += "<div class=\"span4\">Key</div> <div class=\"span5\">Value</div>";
    content += "</div>";
    $.each(data, function() {
        content += "<div class=\"row\">"
        content += "<div class=\"span4\">" + this[0] + "</div>";
        content += "<div class=\"span5\">" + JSON.stringify(this[1]) + "</div>";
        content += "</div>";
    });
    $("#collection-data").append(content);
};

