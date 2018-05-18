var FLOOD_LAYER = "floodLayer";
var BUILDINGS_LAYER = "affectedBuildingsLayer";
var SAFEZONES_LAYER =  "safezonesLayer";

var BUILDING_SIZE = 35;

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function()
{
    console.log("SocketIO connected");
    console.log("Loading default images");
    socket.emit("loadBeforeImage", {});
    socket.emit("loadAfterImage", {});
    socket.emit("loadMapImage", {});

    socket.emit("decide"); socket.emit("act");
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

socket.on("updateModel", function(model)
{
    console.log("Update model...");
    //TODO
    //update task list (needs to be implemented on the UI first)
    //update resource readout
    //update resource locations on map
    //update building locations on map
    //update affected persons on map

    var model = $.parseJSON(model);
    $("canvas#main").removeLayers();

    for (var idx in model["affectedBuildings"])
    {
        console.log(model["affectedBuildings"][idx]["location"]["_Location__longitude"],model["affectedBuildings"][idx]["location"]["_Location__latitude"]);
        
        $("canvas#main").drawEllipse(
        {
            layer: true, fillStyle: "rgba(221, 17, 17, 0.5)",
            x: model["affectedBuildings"][idx]["location"]["_Location__longitude"],
            y: model["affectedBuildings"][idx]["location"]["_Location__latitude"],
            width: BUILDING_SIZE, height: BUILDING_SIZE, groups: [BUILDINGS_LAYER]
        });
    }

    for (var idx in model["safehouses"])
    {
        $("canvas#main").drawEllipse(
            {
                layer: true, fillStyle: "rgba(5, 178, 14, 0.5)",
                x: model["safehouses"][idx]["location"]["_Location__longitude"],
                y: model["safehouses"][idx]["location"]["_Location__latitude"],
                width: BUILDING_SIZE, height: BUILDING_SIZE, groups: [SAFEZONES_LAYER]
            });
    }
});


$( document ).ready(function() {
    $("#checkbox-flood-area").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").setLayerGroup(FLOOD_LAYER,
                {
                    visible: true
                });
        }
        else
        {
            $("canvas#main").setLayerGroup(FLOOD_LAYER,
                {
                    visible: false
                });
        }
        $("canvas#main").drawLayers();
    });

    $("#checkbox-affected-buildings").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").setLayerGroup(BUILDINGS_LAYER,
                {
                    visible: true
                });
        }
        else
        {
            $("canvas#main").setLayerGroup(BUILDINGS_LAYER,
                {
                    visible: false
                });
        }
        $("canvas#main").drawLayers();
    });

    $("#checkbox-safe-zones").change(function()
    {
        if(this.checked)
        {
            $("canvas#main").setLayerGroup(SAFEZONES_LAYER,
                {
                    visible: true
                });
        }
        else
        {
            $("canvas#main").setLayerGroup(SAFEZONES_LAYER,
                {
                    visible: false
                });
        }
        $("canvas#main").drawLayers();
    });

    $("canvas#main").addLayer({name: FLOOD_LAYER, fillStyle: "rgba(41, 148, 219, 0.5)", type:"rectangle", x: 100, y: 100, width: 200, height: 250}).drawLayers();
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