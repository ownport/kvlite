$(document).ready( function() {
    get_collections(0);
});

function get_collections(page) {

    $.getJSON("/collections").done(function(json) {
        if (json.collections.length > 0) {
            
            $('#collections-list').empty();
            $.each(json.collections, function() {
                var collection = "<li><a class=\"collection-name\" role=\"menuitem\" tabindex=\"-1\" href=\"#\">";
                collection += this + "</a></li>";
                $("#collections-list").append(collection);
            });
                        
            $(".collection-name").click(function() {
            
                var collection_name = this.text;

                $("#current-collection-menu").empty();
                $("#current-collection-menu").append(
                    "<li><a role=\"menuitem\" tabindex=\"-1\" href=\"#\" id=\"create-new-item\" data-toggle=\"modal\" data-target=\"#modal-edit-form\">New item</a></li>"
                );                
                $("#create-new-item").click(function() {
                
                    show_edit_form("NEW");
                
                });

                $("#current-collection").html(collection_name + "<b class=\"caret\">");
                get_data(collection_name, page);
            });
        }
    });

};

function get_data(collection_name, page) {

    $.getJSON("/collection/" + collection_name + "/page/" + page).done(function(json) {

        $(".collection-data-pages").empty();
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

/* 
function show_data_as_collapse(data)
*/
function show_data_as_collapse(data) {
    
    $("#collection-data").empty();
    var content = "<div class=\"accordion\" id=\"collection-data-accordion\">";
    $.each(data, function() {
        content += "<div class=\"accordion-group\">";
        content += "<div class=\"accordion-heading\">";
        content += "<a class=\"accordion-toggle\" data-toggle=\"collapse\" ";
        content += "data-parent=\"#collection-data-accordion\"";
        content += "href=\"#" + this[0] +"\">" + this[0] + "</a>";
        content += "</div>"; // <div class="accordion-heading">
        content += "<div id=\"" + this[0] + "\" class=\"accordion-body collapse\">";
        content += "<div class=\"accordion-inner\">";
        content += JSON.stringify(this[1])
        content += "<p><div class=\"btn-group\">";
        content += "<button class=\"btn item-edit\" value=\"" + this[0];
        content += "\" data-toggle=\"modal\" data-target=\"#modal-edit-form\">Edit</button>";
        content += "<button class=\"btn item-delete\" value=\"" + this[0] + "\">Delete</button>";
        content += "</div></p>"; // <div class="btn-group">
        content += "</div>"; // <div class="accordion-inner">
        content += "</div>"; // <div class="accordion-body collapse">
        content += "</div>"; // <div class="accordion-group">              
    });
    content += "</div>"; // <div class="accordion" id="collection-data-accordion">
    $("#collection-data").append(content);
    
    $(".item-edit").click(function () {
        show_edit_form(this.value);
    });
    
    $(".item-delete").click(function () {
        console.debug(this.value);
    });
};

function show_pagination(page, last_page) {

    var left_edge = 3;
    var right_edge = 3;
    page = parseInt(page);
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
        
    for (i = begin_page; i <= end_page; i++) {
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

function show_edit_form(key) {

    var current_collection = $("#current-collection").text();
    
    $("#edit-form-key").empty();
    $("div#item-editor").remove();
    $("div.modal-body").append("<div id=\"item-editor\"> </div>");

    var item_editor = ace.edit("item-editor");
    item_editor.setTheme("ace/theme/clouds");
    item_editor.getSession().setMode("ace/mode/json");
    item_editor.getSession().setUseWrapMode(true);  
    
    if (key == "NEW") {
        
        $.getJSON("/key").done( function(json) {
            if (json.status == "OK") {
                $("#edit-form-key").append(json.key);            
            }
        });
        
    } else {
        $.getJSON("/collection/" + current_collection + "/item/" + key).done( function(json) {
        
            $("#edit-form-key").append(json.item.key);        
            // $("div#item-editor").append(JSON.stringify(json.item.value, null, 4));
            item_editor.getSession().setValue(JSON.stringify(json.item.value, null, 4));
        });    
    };
    
    $("#submit-item-changes").click(function() {
        
        console.debug("submit, key: " + $("#edit-form-key").text());
        console.debug("submit, value: " + item_editor.getSession().getValue());
        // Hide the modal
        $("#modal-edit-form").modal('hide');
    });
    
};
    
