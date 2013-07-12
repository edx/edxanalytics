
/* Render views over time visualization */
function drawTimeVis(dataset){
    var w = visWidth;
    var h = visHeight;
    // Data format: array of [date, count] entries
    // e.g., dataset[0] ==> "2013-03-01": 34

    keys = dataset.map(function(d) { return d[0]; });
    values = dataset.map(function(d) { return d[1]; });
    d3.selectAll("svg.time-chart").remove();
    var xScale = d3.scale.ordinal().domain(keys).rangePoints([0, w]);
    var yScale = d3.scale.linear().domain([ 0, d3.max(values) ]).range([h, 0]);

    var barPadding = 1;
    var chart = d3.select("#time-vis").append("svg")
                .attr("class", "chart time-chart")
                .attr("width", w)
                .attr("height", h);
            // .append("g")
            //     .attr("transform", "translate(0,30)");

    // Show tooltips on mouseover
    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text("Tooltip");

    var line = d3.svg.line()
        .x(function(d, i){ return xScale(i); })
        .y(function(d){ return yScale(d[1]); });
        // .on("mouseover", function(d){
        //     return tooltip.text(d.value[0] + ": " + d.value[1] + " views").style("visibility", "visible");
        // })
        // .on("mousemove", function(d){
        //     return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        // })
        // .on("mouseout", function(d){
        //     return tooltip.style("visibility", "hidden");
        // });

    // chart.selectAll("path")
    //     .data(d3.entries(dataset))
    //     .enter().append("path")    
    //     .attr("d", line(dataset))
        // .on("mouseover", function(d){
        //     console.log(d);
        //     return tooltip.text(d.value[0] + ": " + d.value[1] + " views").style("visibility", "visible");
        // })
        // .on("mousemove", function(d){
        //     return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        // })
        // .on("mouseout", function(d){
        //     return tooltip.style("visibility", "hidden");
        // });
    // Add histogram
    chart.selectAll("rect")
        .data(d3.entries(dataset))
        .enter().append("rect")
        .attr("x", function(d, i){ return i * (w / keys.length); })
        .attr("y", function(d){ return yScale(d.value[1]); })
        .attr("width", w / keys.length - barPadding)
        .attr("height", function(d){ return h - yScale(d.value[1]); })
        // .on("click", rectClickHandler)
        .on("mouseover", function(d){
            return tooltip.text(d.value[0] + ": " + d.value[1] + " views").style("visibility", "visible");
        })
        .on("mousemove", function(d){
            return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        })
        .on("mouseout", function(d){
            return tooltip.style("visibility", "hidden");
        });

    // Add axes
    var padding = 0;
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .tickValues(xScale.domain().filter(function(d,i){
            // only showing the first day of each month
            return d.substr(-2) == "01";
        }));
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(3);
    chart.append("g")
        .attr("class", "axis x-axis")
        .attr("transform", "translate(0," + (h - padding) + ")")
        .call(xAxis);
    chart.append("g")
        .attr("class", "axis y-axis")
        //.attr("transform", "translate(" + padding + ",0)")
        .call(yAxis);

    return chart;
}


/* Add event handlers for tab menu and visualization options */
function bindEvents(){
    $("#tabs .tab-item").click(function(){
        if ($(this).hasClass("active"))
            return;
        $(".tab-item").removeClass("active");
        $(this).addClass("active");
        $("section").hide();
        if ($(this).attr("data-mode") == "summary"){
            $("#stats").show();
            $("#videos").show();
        } else if ($(this).attr("data-mode") == "views"){
            $("#time-vis").show();
        }
        return false;
    });
    bindSortableTableEvents();
}


/* Get aggregate value for the given field */
function get_total(field){
    var result = 0;
    for (var index in data){
        result += data[index][field];
    }
    return result;
}


/* Get the value for the given (field, id) combination */
function get_value_by_id(field, video_id){
    var entry = null;
    for (var index in data){
        if (data[index]["video_id"] == video_id)
            entry = data[index];
    }
    return entry[field];
}


/* Display summary stats */
function displayStats(){
    $(".views .stat").text(get_total("view_count"));
    var num_users = get_total("unique_student_count");
    $(".unique-views .stat").text(num_users);
    // $(".unique-views .substat").text("x% of total enrolled");
    $(".complete-count .stat").text(get_total("completion_count"));
    $(".complete-count .substat").text("completion rate: " + (get_total("completion_count")*100/num_users).toFixed(1) + "%");
    // $(".replay-count").text(getObjectSize(replay_users) + 
    //     " (" + (getObjectSize(replay_users)*100/num_users).toFixed(1) + "% of all viewers)");
    // $(".skip-count").text(getObjectSize(skip_users) + 
    //     " (" + (getObjectSize(skip_users)*100/num_users).toFixed(1) + "% of all viewers)");
    $(".views-per-student .stat").text((get_total("view_count") / num_users).toFixed(2));
    $(".watching-time .stat").text(formatSeconds(get_total("total_watching_time") / num_users));
    // $(".watching-time .substat").text("video length: " + formatSeconds(duration));    
}

/* Display information for the list of videos */
function displayVideos(){
    $.each(videos, function(){
        // console.log($(this), this["video_id"]);
        var num_users = get_value_by_id("unique_student_count", this["video_id"]);
        var url = "video_single?vid=" + this["video_id"];
        var $row = $("<tr/>");
        $("<td/>").html("<a href='" + url + "'>" + this["video_name"] + "</a>").appendTo($row);
        $("<td/>").text(get_value_by_id("view_count", this["video_id"])).appendTo($row);
        $("<td/>").text(formatSeconds(get_value_by_id("total_watching_time", this["video_id"]) / num_users)).appendTo($row);
        $row.appendTo($("#videos-table"));
    });
}


/* Process the aggregate data for views over time vis */
function visualize(){
    // TODO: currently very inefficient way of merging multiple arrays with 
    // potentially non-matching date ranges.
    var tempData = {};
    $.each(videos, function(){
        var views = get_value_by_id("daily_view_counts", this["video_id"]);
        for (var i in views){
            if (views[i][0] in tempData)
                tempData[views[i][0]] += views[i][1];
            else
                tempData[views[i][0]] = views[i][1];
        }
    });
    var keys = Object.keys(tempData);
    keys.sort();
    var processedData = [];
    var i;
    var len = keys.length;
    for (i=0; i<len; i++){
        var entry = [];
        entry[0] = keys[i];
        entry[1] = tempData[keys[i]];
        processedData.push(entry);
    }
    drawTimeVis(processedData);
}


/* Init routine that adds event handlers, displays info, and sets initial options */
function init(){
    bindEvents();
    displayStats();
    displayVideos();
    visualize();
    // by default, click the first item
    $("#tabs a").first().trigger("click");
    $("#vis-options a").first().trigger("click");
    $("#videos-table th").first().trigger("click");
}
