"use strict";

var svg_width = 800;
var svg_height = 400;
var xAxis = null;
var yAxis = null;
var mu_b = 2*Math.PI / 12.0;
var transition_duration = 250;


// type deve ser "mvdr", "music" ou "fourrier"
function updateChart(type, data) {
    var svg = d3.select("svg")
        .attr("width", svg_width)
        .attr("height", svg_height);

    var xPadding = 20;
    var yPadding = 20;
    
    var minAngle = d3.min(data, function(d) {return d.angle;});
    var maxAngle = d3.max(data, function(d) {return d.angle;});

    var minSpectrum = d3.min(data, function (d) {return d[type];});
    var maxSpectrum = d3.max(data, function (d) {return d[type];});
    
    var xScale = d3.scaleLinear()
        .domain([minAngle/mu_b, maxAngle/mu_b])
        .range([2*xPadding, svg_width-xPadding]);
    var yScale = d3.scaleLinear()
        .domain([minSpectrum, maxSpectrum])
        .range([svg_height-2*yPadding, yPadding]);

    var pointsgroup = svg.selectAll(".scatter-plot")
        .data([data]);
    pointsgroup = pointsgroup.enter()
        .append("g")
        .attr("class", "scatter-plot")
        .merge(pointsgroup);
    
    var points = pointsgroup.selectAll(".point")
        .data(function(d) {return d;});
    points = points.enter()
        .append("circle")
        .attr("class", "point")
        .attr("r", 1.5)
        .attr("cx", function(d, i){return xScale(d.angle/mu_b);})
        .attr("cy", function (d, i) {return yScale(d[type]);})
        .merge(points);
    points.transition()
        .duration(transition_duration)
        .attr("cx", function(d, i){return xScale(d.angle/mu_b);})
        .attr("cy", function (d, i) {return yScale(d[type]);});
    
    var line = d3.line()
        .x(function(d, i){return xScale(d.angle/mu_b);})
        .y(function (d, i) {return yScale(d[type]);});
    
    var path = svg.selectAll("path").data([data]);
    path = path.enter().append("path")
        .attr("class", "line")
        .merge(path);
    path.transition()
        .duration(transition_duration)
        .attr("d", line);
    
    
    // Eixo x
    if (xAxis === null) {
        xAxis = svg.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + yScale(0) + ")")
            .call(d3.axisBottom(xScale));
        var xAxisLabel = svg.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate({x},{y})".replace("{x}", svg_width/2).replace("{y}", svg_height-yPadding/3))
            //.attr("transform", "translate("+ (svg_width/2) +","+(svg_height-(yPadding/3))+")")  // centre below axis
            .text("Spatial Separation (normalized)");
    }
    else {
        svg.select(".axis--x").call(xScale);
    }

    if (yAxis === null) {
        yAxis = svg.append("g")
            .attr("class", "axis axis--y")
            .attr("transform", "translate(" + 2*xPadding + ", 0)")
            .call(d3.axisLeft(yScale));
    }
    else {
        svg.select(".axis--y").call(yScale);
    }
    
}


function get_radio_button_value(radio_name) {
    var nodes = nodes = document.getElementsByName(radio_name);
    for (var i=0; i < nodes.length; i++) {
        if (nodes[i].checked === true) {
            break;
        }
    }
    return nodes[i].value;
}


function get_data_filename() {
    var seps = ["2", "1", "0.5", "0.1"];
    var snr_value = get_radio_button_value("snr");
    //var spectrum_type = get_radio_button_value("spectrum_type");
    //var separation = get_radio_button_value("separation");
    var separation = parseFloat(document.getElementById("sep_slider").value).toFixed(1);

    var json_file = "jsondata/data_snr_{snr}_sep_{sep}.json"
        .replace("{snr}", snr_value)
    //.replace("{sep}", seps.indexOf(separation));
    .replace("{sep}", separation);
    return json_file;
}


function handle_radio_button_change() {
    var updateChartBounded = updateChart.bind(null, get_radio_button_value("spectrum_type"));
    var json_file = get_data_filename();

    d3.json(json_file, updateChartBounded);
}


function update_sep_output_value(value) {
	document.querySelector('#sep_value').value = parseFloat(value).toFixed(1);
}


// Gera plot de acordo com os valores nos radio buttons
handle_radio_button_change();
