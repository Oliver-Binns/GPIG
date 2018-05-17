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

});

//wait for the image to load before setting the canvas size and attempting to draw
$("#beforeImage").on('load', function(){
    $("canvas#main")[0].width = $("#beforeImage").width();
    $("canvas#main")[0].height = $("#beforeImage").height();

    $("canvas#main").drawArc(
        {
            fillStyle: "blue",
            x: 100,
            y: 100,
            radius: 40
        }
    );
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