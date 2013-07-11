
/* Move the player to the selected region to sync with the vis */
function rectClickHandler(d, i){
    var second = Math.floor(d3.mouse(this)[0] * duration / visWidth);
    player.seekTo(second);
}


/* Progress the play bar as the video advances */
function moveLine(currentTime){
    var chart = d3.selectAll("svg.play-chart");
    if (chart.length === 0)
        return;
    var curPosition = chart.attr("width") * currentTime / duration;
    chart.selectAll(".playbar")
        .transition()
        .duration(0)
        .attr("x1", curPosition)
        .attr("x2", curPosition);
}


/* Render the heatmap visualization */
function drawPlayVis(dataset, duration){
    var w = visWidth;
    var h = visHeight;
    d3.selectAll("svg.play-chart").remove();
    var xScale = d3.scale.linear().domain([0, duration]).range([0, w]);
    var yScale = d3.scale.linear().domain([0, d3.max(dataset)]).range([h, 0]);

    // margin = 20,
    // y = d3.scale.linear().domain([0, d3.max(data)]).range([0 + margin, h - margin]),
    // x = d3.scale.linear().domain([0, data.length]).range([0 + margin, w - margin])

    var barPadding = 0;
    var chart = d3.select("#play-vis").append("svg")
                .attr("class", "chart play-chart")
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
        .y(function(d){ return yScale(d); });

    // chart.selectAll("path")
    //     .data(dataset)
    //     .enter().append("path")    
    //     .attr("d", line(dataset));

    // chart.append("svg:path")
    //     .data(dataset)
    //     .attr("d", line(dataset))
    //     .on("click", rectClickHandler);
        // .on("mouseover", function(d, i){
        //     console.log(this, d, i);
        //     return tooltip.text("at " + formatSeconds(d.key) + " count: " + d.value).style("visibility", "visible");
        // })
        // .on("mousemove", function(d){
        //     return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        // })
        // .on("mouseout", function(d){
        //     return tooltip.style("visibility", "hidden");
        // });   
    chart.on("click", rectClickHandler);

    // // Add histogram
    chart.selectAll("rect")
        .data(dataset)
        .enter().append("rect")
        .attr("x", function(d, i){ return i * (w / dataset.length); })
        .attr("y", yScale)
        .attr("width", w / dataset.length - barPadding)
        .attr("height", function(d){ return h - yScale(d); })
        // .on("click", rectClickHandler)
        .on("mouseover", function(d, i){
            return tooltip.text("at " + formatSeconds(i) + " count: " + d).style("visibility", "visible");
        })
        .on("mousemove", function(d){
            return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        })
        .on("mouseout", function(d){
            return tooltip.style("visibility", "hidden");
        });

    // Add playbar
    chart.append("line")
        .attr("class", "playbar")
        .attr("x1", 0)
        .attr("x2", 0)
        .attr("y1", 0)
        .attr("y2", h);
        // .call(dragLine);

    // chart.selectAll("text")
    //     .data(dataset)
    // .enter().append("text")
    //     .text(function(d){ return Math.floor(d); })
    //     .attr("x", function(d, i){ return i * (w / dataset.length)+3; })
    //     .attr("y", function(d){ return h - (d*amplifier) - 5; });

    // Add axes
    var padding = 0;
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(5)
        .tickFormat(formatSeconds);
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



function drawTimeVis(dataset){
    var w = visWidth;
    var h = visHeight;
    // Data format: array of [date, count] entries
    // e.g., dataset[0] ==> "2013-03-01": 34

    keys = dataset.map(function(d){ return d[0]; });
    values = dataset.map(function(d){ return d[1]; });
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


// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
function onYouTubeIframeAPIReady() {
  player = new YT.Player('ytplayer', {
    height: '330',
    width: '540',
    videoId: video_id,
    events: {
      'onReady': onPlayerReady
      // 'onStateChange': onPlayerStateChange
    }
  });
}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
    // event.target.playVideo();
    setInterval(updatePlayerInfo, 600);
}


// Update the current playbar in the vis
function updatePlayerInfo(){
    // Conditions: player should have been initialized, player should be playing, and duration should be available
    if (player && YT.PlayerState.PLAYING && duration > 0){
        moveLine(player.getCurrentTime());
    }
}


/*
    The API calls this function when the player's state changes.
    The function indicates that when playing a video (state=1),
    the player should play for six seconds and then stop.

function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING) {
    // Accurate information available only once the player starts playing
    if (duration == 0){
        duration = player.getDuration();
        event.target.stopVideo();
        init();
    }
  }
}
*/


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
            $("#speed").show();
        } else if ($(this).attr("data-mode") == "heatmap"){
            $("#play-vis").show();
        } else if ($(this).attr("data-mode") == "views"){
            $("#time-vis").show();
        }
        return false;
    });

    $("#vis-options a").click(function(){
        console.log($(this).text(), "clicked");
        $("#vis-options a").removeClass("active");
        $(this).addClass("active");
        var mode = $(this).attr("data-mode");
        // var processedData = processData(data, mode, binSize, duration);
        var processedData = data[mode];
        drawPlayVis(processedData, duration);

        // processedData = processTimeData(data);
        processedData = data["daily_view_counts"];
        drawTimeVis(processedData);
        // redrawVis(chart, processedData, duration, visWidth, visHeight);
        return false;
    });
}

/* Display summary stats */
function displayStats(){
    $(".views .stat").text(data["view_count"]);
    var num_users = data["unique_student_count"];
    $(".unique-views .stat").text(num_users);
    // $(".unique-views .substat").text("x% of total enrolled");
    $(".complete-count .stat").text(data["completion_count"]);
    $(".complete-count .substat").text("completion rate: " + (data["completion_count"]*100/num_users).toFixed(1) + "%");
    // $(".replay-count").text(getObjectSize(replay_users) + 
    //     " (" + (getObjectSize(replay_users)*100/num_users).toFixed(1) + "% of all viewers)");
    // $(".skip-count").text(getObjectSize(skip_users) + 
    //     " (" + (getObjectSize(skip_users)*100/num_users).toFixed(1) + "% of all viewers)");
    $(".views-per-student .stat").text((data["view_count"] / num_users).toFixed(2));
    $(".watching-time .stat").text(formatSeconds(data["total_watching_time"] / num_users));
    $(".watching-time .substat").text("video length: " + formatSeconds(duration));
}


function displayPlayRates(){
    var total_playrate_counts = 0;
    var sorted_playrate_counts = [];
    for (var rate in data["playrate_counts"]){
        total_playrate_counts += data["playrate_counts"][rate];
        // replace _ with . in the speed display because Mongo doesn't allow . in the key
        sorted_playrate_counts.push([rate.replace("_", ".") + "x", data["playrate_counts"][rate]]);
    }
    sorted_playrate_counts.sort(function(a, b){
        return b[1] - a[1];
    });
    $.each(sorted_playrate_counts, function(){
        var $row = $("<tr/>");
        $("<td/>").text(this[0]).appendTo($row);
        $("<td/>").text(this[1]).appendTo($row);
        var percentage = (100.0 * this[1] / total_playrate_counts).toFixed(2);
        var $bar = $("<span/>").addClass("speed-bar").width(percentage + "%");
        $("<td/>").append($bar).append(percentage + "%").appendTo($row);
        $row.appendTo($("#speed-table"));
    });
}

/* display video title */
function displayTitle(video_id){
    for (var index in videos){
        if (video_id == videos[index]["video_id"])
            $(".video-title").text(videos[index]["video_name"]);
    }
}


/* get duration information from the videos data */
function getDuration(video_id){
    var value = 0;
    for (var index in videos){
        if (video_id == videos[index]["video_id"])
            value = videos[index]["duration"];
    }
    return value;
}


/* Add prev and next links in the nav bar */
function displayNav(video_id){
    for (var index in videos){
        if (video_id == videos[index]["video_id"]){
            var prev_index = 0;
            if (index === 0)
                prev_index = videos.length - 1;
            else
                prev_index = parseInt(index, 10) - 1;
            $(".nav .prev a").attr("href", "video_single?vid=" + videos[prev_index]["video_id"]);
            var next_index = 0;
            if (index == videos.length - 1)
                next_index = 0;
            else
                next_index = parseInt(index, 10) + 1;
            $(".nav .next a").attr("href", "video_single?vid=" + videos[next_index]["video_id"]);

        }
    }
}


/* Init routine that adds event handlers, displays info, and sets initial options */
function init(){
    bindEvents();
    duration = getDuration(video_id);
    displayTitle(video_id);
    displayNav(video_id);
    displayStats();
    displayPlayRates();
    // by default, click the first item
    $("#tabs a").first().trigger("click");
    $("#vis-options a").first().trigger("click");
}

