var FLOOD_LAYER = "floodLayer";
var BUILDINGS_LAYER = "affectedBuildingsLayer";
var SAFEZONES_LAYER =  "safezonesLayer";

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function()
{
    console.log("SocketIO connected");
    console.log("Loading default images");
    socket.emit("loadBeforeImage", {});
    socket.emit("loadAfterImage", {});
    socket.emit("loadMapImage", {});
});

socket.on('displayBeforeImage', function(imgStr)
{
    $("#beforeImage").attr("src", "data:image/jpg;base64,"+imgStr);
    
});

socket.on('displayAfterImage', function(imgStr)
{
    $("#afterImage").attr("src", "data:image/jpg;base64,"+imgStr);
});

socket.on('displayMapImage', function(imgStr)
{
    $("#mapImage").attr("src", "data:image/jpg;base64,"+imgStr);
});

socket.on("updateTaskList", function(taskList)
{
    console.log("new task list: " + taskList)
});


$( document ).ready(function() {
    $("#checkbox-flood-area").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").getLayer(FLOOD_LAYER).visible = true;
        }
        else
        {
            $("canvas#main").getLayer(FLOOD_LAYER).visible = false;
        }
        $("canvas#main").drawLayers();
    });

    $("#checkbox-affected-buildings").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").getLayer(BUILDINGS_LAYER).visible = true;
        }
        else
        {
            $("canvas#main").getLayer(BUILDINGS_LAYER).visible = false;
        }
        $("canvas#main").drawLayers();
    });

    $("#checkbox-safe-zones").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").getLayer(SAFEZONES_LAYER).visible = true;
        }
        else
        {
            $("canvas#main").getLayer(SAFEZONES_LAYER).visible = false;
        }
        $("canvas#main").drawLayers();
    });

    $("canvas#main").addLayer({name: FLOOD_LAYER, fillStyle: "rgba(41, 148, 219, 0.5)", type:"rectangle", x: 100, y: 100, width: 200, height: 250})
        .addLayer({name: BUILDINGS_LAYER, fillStyle: "rgba(221, 17, 17, 0.5)", type:"rectangle", x: 300, y: 300, width: 200, height: 250})
        .addLayer({name: SAFEZONES_LAYER, fillStyle: "rgba(5, 178, 14, 0.5)", type:"rectangle", x: 500, y: 500, width: 200, height: 250}).drawLayers();
});

//wait for the image to load before setting the canvas size and attempting to draw
$("#beforeImage").on('load', function(){
    $("canvas#main")[0].width = $("#beforeImage").width();
    $("canvas#main")[0].height = $("#beforeImage").height();
    $("canvas#main").drawLayers();
});



function showBeforeImage()
{
    $("#beforeImage").show();
    $("#afterImage").hide();
    $("#mapImage").hide();
}

function showAfterImage()
{
    $("#beforeImage").hide();
    $("#afterImage").show();
    $("#mapImage").hide();
}

function showMapImage()
{
    $("#beforeImage").hide();
    $("#afterImage").hide();
    $("#mapImage").show();
}