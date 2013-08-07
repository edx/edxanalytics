/* Helper Functions */

/* Return the size of an object, because .length doesn't work for objects */
function getObjectSize(obj){
    var size = 0;
    var key;
    for (key in obj){
        if (obj.hasOwnProperty(key))
            size++;
    }
    return size;
}


/* Return a human-readable format for the number of seconds */
function formatSeconds(sec){
    var s = Math.round(sec%60);
    return "" + Math.floor(sec/60) + ":" + (s<=9 ? '0' + s : s);
}


/* Check if the string is a number */
function isNumber(n){
    return !isNaN(parseFloat(n)) && isFinite(n);
}


/* Sort table by the table ID and column index. */
function sortTable(id, index, is_first_header, is_ascending){
    var tbl = document.getElementById(id).tBodies[0];
    var store = [];
    var i = is_first_header ? 1 : 0;
    var len;
    for(len = tbl.rows.length; i < len; i++){
        var row = tbl.rows[i];
        var sortnr = row.cells[index].textContent || row.cells[index].innerText;
        store.push([sortnr, row]);
    }
    store.sort(function(x, y){
        var val = 0;
        if (isNumber(x[0]) && isNumber(y[0]))
            return parseFloat(x[0]) - parseFloat(y[0]);
        if (x[0] > y[0])
            val = 1;
        if (x[0] < y[0])
            val = -1;
        if (!is_ascending)
            val *= -1;
        return val;
    });
    i = is_first_header ? 1 : 0;
    for(len = store.length; i < len; i++){
        tbl.appendChild(store[i][1]);
    }
    store = null;
}


function bindSortableTableEvents(){
    $("table.sortable th").click(function(){
        var index = $(this).index();
        var $option = $(this).find(".sort-option");
        var sort_class = "";
        var is_ascending = true;
        var table_id = $(this).closest("table").attr("id");
        // alternate between asc and desc sorting
        if ($option.hasClass("active")) {
            is_ascending = !($option.hasClass("ascending"));
            sort_class = $option.hasClass("ascending") ? "descending" : "ascending";
        } else {
            is_ascending = $option.attr("data-default") == "ascending";
            sort_class = $option.attr("data-default");
        }
        $("#" + table_id + " .sort-option").text("");
        $("#" + table_id + " .sort-option").removeClass("active ascending descending");
        $option.addClass("active " + sort_class);
        if (is_ascending)
            $option.html("&#8593;");
        else
            $option.html("&#8595;");
        sortTable(table_id, index, true, is_ascending);
    });

    $("table.sortable th").mouseenter(function(){
        var $option = $(this).find(".sort-option");
        var is_ascending = true;
        // alternate between asc and desc sorting
        if ($option.hasClass("active")) {
            is_ascending = !($option.hasClass("ascending"));
        } else {
            is_ascending = $option.attr("data-default") == "ascending";
        }
        if (is_ascending)
            $option.html("&#8593;");
        else
            $option.html("&#8595;");
    });

    $("table.sortable th").mouseleave(function(){
        var $option = $(this).find(".sort-option");
        var is_ascending = true;
        // alternate between asc and desc sorting
        if ($option.hasClass("active")) {
            // check if preview is on or not
            is_ascending = !($option.hasClass("ascending"));
            if (is_ascending)
                $option.html("&#8595;");
            else
                $option.html("&#8593;");
        } else {
            is_ascending = $option.attr("data-default") == "ascending";
            $option.html("&nbsp;");
        }
    });    
}
