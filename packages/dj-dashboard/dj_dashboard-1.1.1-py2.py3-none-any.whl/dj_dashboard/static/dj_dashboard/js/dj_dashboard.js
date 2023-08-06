function removeClick(item){
    // get the id
    dashboard_id = item.id
    dashboard_id = dashboard_id.replace("remove_", "");
    // create a hidden input field with the id
    $("#form_dashboard").append('<input type="hidden" name="remove-widget" value="'+dashboard_id+'" />')
    // remove it from the grid
    var grid = $('.grid-stack').data('gridstack');
    grid.removeWidget($(item).parents().eq(1));
};

function editClick(edit_url, w, h){
    // arguments with default values PRE ES2015
    w = typeof w !== 'undefined' ? w : 750;
    h = typeof h !== 'undefined' ? h : 550;

    var left = (screen.width/2)-(w/2);
    var top = (screen.height/2)-(h/2);
    return window.open(edit_url, "", 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=1, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+top+', left='+left);
};

function resizeDashboardBar() {
  if ($(window).width() >= 1200) {
      $('#dj_dashboard').css({'width': '78%'});
    } else if ($(window).width() >= 980){
      $('#dj_dashboard').css({'width': '73%'});
    } else {
        $('#dj_dashboard').css({'width': '66%'});
    }
}

function switchEditMode() {
    if (editMode == true) {
        if (allowMove == true) {
            // Edit Controls activated
            $('.grid-stack').data('gridstack').enableMove(true);
            $('.grid-stack').data('gridstack').enableResize(true);
        } else {
            // Edit Controls deactivated
            $('.grid-stack').data('gridstack').enableMove(false);
            $('.grid-stack').data('gridstack').enableResize(false);
        }
        // Show dropzone
        $('#dropzone').show()
        // Reduce width of dashboard
        resizeDashboardBar();
        $( window ).resize(function() {
            resizeDashboardBar();
        });

        // Show Edit controls
        $('.editControl').show();  // The configuration Form
        $('.editControlTrash').show();  // The remove Icon
    } else {
        // Edit Controls deactivated
        $('.grid-stack').data('gridstack').enableMove(false);
        $('.grid-stack').data('gridstack').enableResize(false);
        // Edit controls deactivated
        $('#dj_dashboard').css({'width': '100%'});
        $('.editControl').hide();  // The configuration Form
        $('.editControlTrash').hide();  // The remove Icon
    }
};

function saveWidgets() {
    // Collect all data from all grid items
    var res = _.map($('.grid-stack .grid-stack-item:visible'), function (el) {
        el = $(el);
        var node = el.data('_gridstack_node');
        // Set the height to minimal height 2 if the content can grow
        node_height = node.height
        if (el.attr('content_can_grow') == 1) {
            node_height = 2
        }
        return {
            id: el.attr('id'),
            content_can_grow: el.attr('content_can_grow'),
            x: node.x,
            y: node.y,
            width: node.width,
            height: node_height
        };
    });
    // load values into form field: widgets
    $('#widgets').val(JSON.stringify(res));
    // Submit on the form
    $('form[id="form_dashboard"]').submit();
};


function resetToDefault(){
    // create a hidden input field with
    $("#form_dashboard").append('<input type="hidden" name="reset-default" value="1" />')
    $('form[id="form_dashboard"]').submit();
};

/* DRAG & DROP funtionality */
function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev, ui) {
    ev.preventDefault();
    var data = ui.draggable.attr('id');
    var title = ui.draggable.attr('title');
    var x = ev.pageX;
    $('#add-widget-select').val(data);
    $('#add-widget-y').val(0);
    $('#add-widget-title').val(title);
    saveWidgets();
}
