var FLOOD_LAYER = "floodLayer";

var FLOOD_LAYER_HEIGHT = 697;
var FLOOD_LAYER_WIDTH  = 1240;
var FLOOD_LAYER_ASPECT = FLOOD_LAYER_WIDTH / FLOOD_LAYER_HEIGHT; 

var BUILDINGS_LAYER = "affectedBuildingsLayer";
var REST_CENTRES_LAYER =  "restCentresLayer";
var RESOURCES_LAYER =  "resourcesLayer";
var PEOPLE_LAYER =  "peopleLayer";

var BUILDING_SIZE = 35;
var RESOURCE_SIZE = 15;

var floodImg = new Image();

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function()
{
    console.log("SocketIO connected");
    console.log("Loading default images");
    socket.emit("loadBeforeImage", {});
    socket.emit("loadAfterImage", {});
    socket.emit("loadMapImage", {});

    let updateloop = window.setInterval(()=>{
        socket.emit("decide"); 
        socket.emit("stepSim");
    },100)

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

function scaleX(x)
{
    var sX = $("#beforeImage").width() / FLOOD_LAYER_WIDTH;
    return x * sX;
}

function scaleY(y)
{
    var sY = $("#beforeImage").height() / FLOOD_LAYER_HEIGHT;
    return y * sY;
}

function updateResourceBars(model)
{
    $(".progress-bar#boats").css("width", model.assignedBoats+"%");
    $(".progress-bar#paramedics").css("width", model.assignedParamedics+"%");
    $(".progress-bar#firefighters").css("width", model.assignedResponders+"%");
}

//Used to clear all information except for the flood map data
//This is done to prevent flickering caused by redrawing the flood data image
function preUpdateClearCanvas()
{
    $("canvas#main").removeLayerGroup(BUILDINGS_LAYER)
                    .removeLayerGroup(REST_CENTRES_LAYER)
                    .removeLayerGroup(RESOURCES_LAYER)
                    .removeLayerGroup(PEOPLE_LAYER)
                    .drawLayers()
}

socket.on("updateModel", function(model)
{
    //TODO
    //update task list (needs to be implemented on the UI first)
    //update resource readout
    //update affected persons on map

    var model = $.parseJSON(model);

    //clear the layers and force the canvas to update before the new data is drawn
    preUpdateClearCanvas();

    if($("#checkbox-affected-buildings").prop("checked"))
    {
        for (var idx in model["affectedBuildings"])
        {        
            $("canvas#main").drawEllipse(
            {
                layer: true, fillStyle: "rgba(221, 17, 17, 0.5)",
                x: scaleX(model["affectedBuildings"][idx]["location"]["_Location__longitude"]),
                y: scaleY(model["affectedBuildings"][idx]["location"]["_Location__latitude"]),
                width: BUILDING_SIZE, height: BUILDING_SIZE, groups: [BUILDINGS_LAYER]
            });
        }
    }

    if($("#checkbox-rest-centres").prop("checked"))
    {
        for (var idx in model["safehouses"])
        {
            $("canvas#main").drawEllipse(
                {
                    layer: true, fillStyle: "rgba(5, 178, 14, 0.5)",
                    x: scaleX(model["safehouses"][idx]["location"]["_Location__longitude"]),
                    y: scaleY(model["safehouses"][idx]["location"]["_Location__latitude"]),
                    width: BUILDING_SIZE, height: BUILDING_SIZE, groups: [REST_CENTRES_LAYER]
                });
        }
    }

    if($("#checkbox-resources").prop("checked"))
    {
        for (var idx in model["boats"])
        {
            $("canvas#main").drawImage(
                {
                    layer: true, source: "/static/img/ship.png",
                    x: scaleX(model["boats"][idx]["location"]["_Location__longitude"]),
                    y: scaleY(model["boats"][idx]["location"]["_Location__latitude"]),
                    width: RESOURCE_SIZE, height: RESOURCE_SIZE, groups: [RESOURCES_LAYER]
                });
        }
    
        for (var idx in model["paramedics"])
        {
            $("canvas#main").drawImage(
                {
                    layer: true, source: "/static/img/medkit.png",
                    x: scaleX(model["paramedics"][idx]["location"]["_Location__longitude"]),
                    y: scaleY(model["paramedics"][idx]["location"]["_Location__latitude"]),
                    width: RESOURCE_SIZE, height: RESOURCE_SIZE, groups: [RESOURCES_LAYER]
                });
        }

        for (var idx in model["responders"])
        {
            $("canvas#main").drawImage(
                {
                    layer: true, source: "/static/img/fire-extinguisher.png",
                    x: scaleX(model["responders"][idx]["location"]["_Location__longitude"]),
                    y: scaleY(model["responders"][idx]["location"]["_Location__latitude"]),
                    width: RESOURCE_SIZE, height: RESOURCE_SIZE, groups: [RESOURCES_LAYER]
                });
        }
    }

    if($("#checkbox-flood-area").prop("checked"))
    {
        if(floodImg.src != ("data:image/png;base64,"+model.flood))
        {
            var canvas = $("canvas#main");
            var image = $("#beforeImage");
            
            var image_height = image.height();
            var image_width = image.width();
            
            var image_aspect = image_width / image_height;
            
            //if image fits to height!
            var width = FLOOD_LAYER_ASPECT * image_height / 2;
            var height = image_height / 2;
            var scale = image_height / FLOOD_LAYER_HEIGHT;
            
            //if image fits to width!
            if(image_aspect > FLOOD_LAYER_ASPECT){
                var width = image_width / 2;
                var height = (image_width / 2) / FLOOD_LAYER_ASPECT;
                var scale = image_width / FLOOD_LAYER_WIDTH;
            }
            
            canvas.removeLayer(FLOOD_LAYER).drawLayers();
            floodImg.src = "data:image/png;base64,"+model.flood
             
            canvas.addLayer(
                {
                    type: 'image',
                    source: floodImg,
                    x: width,
                    y: height,
                    scale: scale,
                    fromCenter: true,
                    layer: true,
                    groups: [FLOOD_LAYER]
                }
            )
        }
    }

    updateResourceBars(model);
});


$(document).ready(function() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    
    $("#checkbox-flood-area").change(function()
    {
        setLayerVisibility(FLOOD_LAYER, this.checked);
    });

    $("#checkbox-affected-buildings").change(function()
    {
        setLayerVisibility(BUILDINGS_LAYER, this.checked);
    });

    $("#checkbox-rest-centres").change(function()
    {
        setLayerVisibility(REST_CENTRES_LAYER, this.checked);
    });

    $("#checkbox-resources").change(function()
    {
        setLayerVisibility(RESOURCES_LAYER, this.checked);
    });

    $("#checkbox-people").change(function()
    {
        setLayerVisibility(PEOPLE_LAYER, this.checked);
    });
});

function setLayerVisibility(layer, value){
    var canvas = $("canvas#main");
    canvas.setLayerGroup(layer,
        {
            visible: value
        }
    );
    canvas.drawLayers();
}

//wait for the image to load before setting the canvas size and attempting to draw
$("#beforeImage").on('load', function(){
    $("canvas#main")[0].width = $("#beforeImage").width();
    $("canvas#main")[0].height = $("#beforeImage").height();
    $("canvas#main").drawLayers();
});

function showMap(type){
    var map = $("#" + type + "Image")
    map.show();
    map.siblings('img').hide();
}