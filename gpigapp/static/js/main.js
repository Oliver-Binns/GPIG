var FLOOD_LAYER = "floodLayer";

var FLOOD_LAYER_HEIGHT = 697;
var FLOOD_LAYER_WIDTH  = 1240;
var FLOOD_LAYER_ASPECT = FLOOD_LAYER_WIDTH / FLOOD_LAYER_HEIGHT; 

var BUILDINGS_LAYER = "affectedBuildingsLayer";
var REST_CENTRES_LAYER =  "restCentresLayer";
var RESOURCES_LAYER =  "resourcesLayer";
var PEOPLE_LAYER =  "peopleLayer";

var BUILDING_SIZE = 40;
var RESOURCE_SIZE = 25;

var floodImg = new Image();

var updateLoop;

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function()
{
    console.log("SocketIO connected");
    console.log("Loading default images");
    socket.emit("loadBeforeImage", {});
    socket.emit("loadAfterImage", {});
    socket.emit("loadMapImage", {});

    setUIUpdateInterval(100);

});

function setUIUpdateInterval(ms)
{
    clearInterval(updateLoop);
    updateLoop = window.setInterval(() => 
    {
        socket.emit("observe")
        socket.emit("decide");
        socket.emit("stepSim");
    }, ms);
}

function setServerSpeed(speed)
{
    socket.emit("changeSpeed", speed);
}

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
    $(".progress-bar#rest-centres").css("width", model.remainingRestCentreSpace+"%");
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
    
    var task_container = $("#tasks");
    if(task_container.children().length == 0){
        //Container is empty- create elements
        createTaskView(task_container, "overview", "Overview", true, null, [])
        displayTasks(task_container, model["tasks"]);
    }else{
        //Container is NOT empty, update
        updateTasks(task_container, model["tasks"]);
    }
   

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
    
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
});

function displayTasks(container, tasks){
    for(task of tasks){
        container.append("<hr/>");
        createTaskView(container,
            task["ID"], task["name"], false,
            task["percentComplete"], task["resources"]
        );
    }
}

function updateTasks(container, tasks){
    var task_views = container.children("div");
    var overview_view = [].shift.call(task_views);
    
    task_views.each(function(){
        for(i = 0; i < tasks.length; i++){
            var task = tasks[i];
            
            var task_id = task["ID"];
            if(task_id == this.id){
                tasks.splice(i, 1);
                i--;
                return;
            }
        }
        this.previousSibling.remove();
        this.remove();
    });
    
    displayTasks(container, tasks);
}

function createTaskView(container, uid, name, active, completion, resources){
    var task_view = $('<div id="' + uid + '"><div class="arrow"></div></div>');
    task_view.append("<h1>" + name + "</h1>");
    
    if(active){
        task_view.addClass("active");
    }

    //Status
    if(uid != "overview"){
        task_view.append($("<div class='status'>Status: <span></span></div>"));
    }
    
    //Resources View
    var resources_view = $("<div class='resources'><span>Resources: </span></div>");
    var boats = 0;
    var paramedics = 0;
    var firefighters = 0;
    for(var i = 0; i < resources.length; i++){
        var resource = resources[i];
        if(resource["capacity"] != null){
            boats++;
        }else{
            paramedics++;
        }
    }
    resources_view.append(getResourceLabel("Boats", "ship", boats));
    resources_view.append(getResourceLabel("Paramedics", "medkit", paramedics));
    resources_view.append(getResourceLabel("Firefighters", "fire-extinguisher", firefighters));
    task_view.append(resources_view);
    
    container.append(task_view);
    setStatus(uid, "Pending", "pending");
}

function getResourceLabel(name, icon, count){
    var label = '<span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="top" title="{0}"><i class="fas fa-{1}"></i> {2}</span>';
    label = label.replace("{0}", name).replace("{1}", icon).replace("{2}", count);
    return $(label);
}

function setStatus(task_id, status, class_name, f){
    var statusSpan = $("#" + task_id + " .status span"); 

    statusSpan.removeClass();
    statusSpan.addClass(class_name.toLowerCase());

    statusSpan.nextAll("button").remove();
    if(class_name == "pending"){
        statusSpan.after(' <button onclick="beginAcceptTask(this);" type="button" class="btn btn-sm btn-success"><i class="fas fa-check"></i> Accept</button>');
        statusSpan.after(' <button onclick="beginRejectTask(this);" type="button" class="btn btn-sm btn-danger"><i class="fas fa-times"></i> Reject</button>');
    }else if (class_name === "accepted" || class_name === "rejecting"){
        button = $('<button type="button" class="btn btn-sm btn-info"><i class="fas fa-undo"></i> Undo</button>');
        button.click(f);
        statusSpan.after(button);
        statusSpan.after(' ');
    }

    statusSpan.html(status);
}

function beginAcceptTask(button){
    var id = button.parentElement.parentElement.id;
    
    var count = 5;

    var timer;
    timer = setInterval(function(){
        if(count > 0){
            var text = "Accepted, starting in " + count + "."
            count--;
            setStatus(id, text, "accepted", function(){
                clearInterval(timer);
                setStatus(id, "Pending", "pending");
            });
        }else{
            acceptTask(id);
            setStatus(id, "In Progress", "in-progress");
            clearInterval(timer);
        }
    }, 1000, id, count, timer);
}

function beginRejectTask(button){
    var id = button.parentElement.parentElement.id;
    
    var count = 5;

    var timer;
    timer = setInterval(function(){
        if(count > 0){
            var text = "Rejecting in " + count + "."
            count--;
            setStatus(id, text, "rejecting", function(){
                clearInterval(timer);
                setStatus(id, "Pending", "pending");
            });
        }else{
            rejectTask(id);
            setStatus(id, "Rejected", "rejected");
            clearInterval(timer);
        }
    }, 1000, id, count, timer);
}

function acceptTask(uid)
{
    socket.emit("acceptTask", uid);
    //update UI?
}

function rejectTask(uid)
{
    socket.emit("rejectTask", uid);
    //update UI?
}

function resetSim()
{
    socket.emit("resetSim");
    //update UI?
}

$(document).ready(function() {
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