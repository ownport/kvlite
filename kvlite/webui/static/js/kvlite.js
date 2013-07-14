$(document).ready( function() {
    get_collections(0);
});

function get_collections(page) {

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
                get_data(collection_name, page)
            });
        };
    });

};

function get_data(collection_name, page) {

    $.getJSON("/collection/" + collection_name + "/page/" + page).done(function(json) {

        $("#collection-data-pages").empty();
        $("#collection-data").empty();

        if (json.status == "OK") {
            if (json.data.length > 0) {

                show_pagination(page, json.last_page);                
                show_data_as_collapse(json.data);
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
    var content = "<div class=\"row\">";
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

function show_data_as_collapse(data) {
    
    $("#collection-data").empty();
    var content = "<div class=\"accordion\" id=\"collection-data-accordion\">";
    $.each(data, function() {
        content += "<div class=\"accordion-group\">";
        content += "<div class=\"accordion-heading\">";
        content += "<a class=\"accordion-toggle\" data-toggle=\"collapse\" ";
        content += "data-parent=\"#collection-data-accordion\" href=\"#" + this[0] +"\">";
        content += this[0] + "</a> </div>";
        content += "<div id=\"" + this[0] + "\" class=\"accordion-body collapse\">";
        content += "<div class=\"accordion-inner\">";
        content += JSON.stringify(this[1]) + "</div> </div> </div>";                
    });
    content += "</div>";
    $("#collection-data").append(content);
};

function show_pagination(page, last_page) {

    var left_edge = 3;
    var right_edge = 3;
    var page = parseInt(page);
    var last_page = parseInt(last_page);
    var pagination = "<div class=\"pagination\"><ul>";
    
    var begin_page = 0;
    var end_page = last_page;
    
    $(".collection-data-pages").empty();
    
    if ((page - left_edge) > 0) {
        pagination += "<li><a class=\"selected-page\" href=\"#\">First</a></li>";    
        begin_page = page - left_edge;
        end_page = begin_page + left_edge + right_edge;
        if (end_page > last_page) {
            begin_page = last_page - left_edge - right_edge;
            end_page = last_page;
        };
    } else {
        begin_page = 0;
        end_page = left_edge + right_edge;
    };
        
    for (i = begin_page; i < end_page; i++) {
        if (i == page) {
            pagination += "<li class=\"active\">";
        } else {
            pagination += "<li>";
        };
        
        pagination += "<a class=\"selected-page\" href=\"#\">" + i + "</a></li>";
    }

    if ((page + right_edge) < last_page) {
        pagination += "<li><a class=\"selected-page\" href=\"#\">Last</a></li>";
    };
    pagination += "</ul></div>";

    $(".collection-data-pages").append(pagination);
    $(".selected-page").click(function() {
        var current_collection = $("#current-collection").text();
        var selected_page = this.text;
        if (selected_page == "First") {
            selected_page = 0;
        } else if (selected_page == "Last") {
            selected_page = last_page;
        };
        get_data(current_collection, selected_page);
    });
};
