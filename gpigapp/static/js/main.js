var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function()
{
    console.log("SocketIO connected");
    console.log("Loading default images");
    socket.emit("loadBeforeImage", {});
    socket.emit("loadAfterImage", {});
});

socket.on('displayBeforeImage', function(imgStr)
{
    $("#beforeImage").attr("src", "data:image/jpg;base64,"+imgStr);
    
});

socket.on('displayAfterImage', function(imgStr)
{
    $("#afterImage").attr("src", "data:image/jpg;base64,"+imgStr);
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
}

function showAfterImage()
{
    $("#beforeImage").hide();
    $("#afterImage").show();
}