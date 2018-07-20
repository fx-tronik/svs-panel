$(document).ready(function(){
    $("#btnopenimage").click(function(){openImage();});
    $("#selectedFile").change(function(evt){onFileSelected(evt);});
    $("#btnopenimagefromdisk").click(function(){$('#selectedFile').click();});
    $("#btnclear").click(function(){clearCanvas();});
    $("#btnshow").click(function(){drawAll();});
    $("#checkboxAddZone").click(function(){cb_zone_Clicked();});
    $("#btncanceldraw").click(function(){stopdraw(0);});
    $("#selectZone").change(function(){selectedzonechanged();});
    $("#btndeleteselected").click(function(){deleteZone();});
    $("#btndeleteall").click(function(){deleteAllZones();});
    $("#btnupdate").click(function(){updateproperties();});
    $("#canvasDraw").mouseup(function(evt){CanvasMouseUp(evt);});
    $("#canvasDraw").on({
      mouseup: function(evt){CanvasMouseUp(evt);},
      mousedown: function(evt){CanvasMouseDown(evt);}
    });
    $("#btnsave").click(function(){saveConfig();});
});

class Zone {
    constructor(properties,points) {
        this.Properties = properties;
        this.ZonePoints = points;
        this.Selected = true;
    }

    get Out() {
      return this.ZonePoints;
    }
}
class ZoneProperties {
    constructor(name,width,height) {
        this.ImageHeight = width;
        this.ImageWidth = height;
        this.Name = name;
        this.Type = 1;
    }
}

var canvas_draw = $('#canvasDraw')[0];
var ctx_draw = canvas_draw.getContext('2d');
var canvas_zones = $('#canvasZones')[0];
var ctx_zones = canvas_zones.getContext('2d');
var canvas_img = $('#canvasImg')[0];
var ctx_img = canvas_img.getContext('2d');

var polybegin;
var mouseclicked;
var drawnpoly = [];
var zones = [];

var imageObj = new Image();
imageObj.onload = function() {
  deleteAllZones()
  canvas_img.height = canvas_img.width * imageObj.height / imageObj.width ;
  canvas_draw.height = canvas_img.height;
  canvas_zones.height = canvas_img.height;
  $("#divzones").height(canvas_img.height+10);
  $("#divzones").show();
  ctx_img.drawImage(imageObj, 0, 0, canvas_img.width, canvas_img.height);
}

init();

function init() {
    polybegin = false;
    $("#divzones").hide();
    $("#divzoneprop").hide();
    $("#btncanceldraw").hide();
    return;
}

function CanvasMouseUp(evt) {
  if (mouseclicked) {
    var mousePos = getMousePos(canvas_draw, evt);
      if (mousePos.which == 1) {
        if (polybegin) {
          drawnpoly.push({"x":mousePos.x, "y":mousePos.y});
          drawPoly(drawnpoly,false);
        }
      }
      else if (mousePos.which == 3) {
        stopdraw(1);
      }
  }
  mouseclicked = false;
}
function CanvasMouseDown(evt) {
  var mousePos = getMousePos(canvas_draw, evt);

  if(!$("#checkboxAddZone").prop('checked')) {
    var tempcanvas = document.createElement("CANVAS");
    tempcanvas.height = canvas_img.height;
    tempcanvas.width = canvas_img.width;
    var tempctx = tempcanvas.getContext('2d');
    if (zones.length) {
      for (var i =0; i < zones.length; i++) {
        var points = zones[i].ZonePoints;
        tempctx.clearRect(0, 0, tempcanvas.width, tempcanvas.height);
        tempctx.fillStyle = "red";
        tempctx.beginPath();
        tempctx.moveTo(points[0].x, points[0].y);
        for( item=1 ; item < points.length ; item++ ){tempctx.lineTo( points[item].x , points[item].y )}
        tempctx.closePath();
        tempctx.fill();
        var p = tempctx.getImageData(mousePos.x, mousePos.y, 1, 1).data;
        if (p[0]==255) {
          $("#selectZone option").eq(i).prop("selected", true);
          selectedzonechanged();
          break;
        }
      }
    }
  }
  mouseclicked = true;
}

function getMousePos(canvas, evt) {
    if (evt.pageX != undefined && evt.pageY != undefined) {
        var x = evt.pageX;
		var y = evt.pageY;
	}
	else {
	    x = evt.clientX + document.body.scrollLeft +
				document.documentElement.scrollLeft;
		y = evt.clientY + document.body.scrollTop +
				document.documentElement.scrollTop;
    }
  var rect = canvas.getBoundingClientRect();
	x -= rect.x;
	y -= rect.y;
    return {
        x: parseInt(x),
        y: parseInt(y),
        which: evt.which
    };
}

function drawPoly(points,selected) {
  ctx_draw.clearRect(0, 0, canvas_draw.width, canvas_draw.height);
  ctx_draw.globalAlpha=0.35;
  ctx_draw.fillStyle = "yellow";
  if (selected) ctx_draw.fillStyle = "red";
  ctx_draw.beginPath();
  ctx_draw.moveTo(points[0].x, points[0].y);
  for( item=1 ; item < points.length ; item++ ){ctx_draw.lineTo( points[item].x , points[item].y )}
  ctx_draw.closePath();
  ctx_draw.fill();
  ctx_draw.globalAlpha=1;

  for( item=0 ; item < points.length ; item++ ) {
    ctx_draw.fillStyle = "yellow";
    ctx_draw.beginPath();
    ctx_draw.arc(points[item].x , points[item].y, 3, 0, Math.PI*2, false);
    ctx_draw.closePath();
    ctx_draw.fill();
  }

}
function drawAll() {
    clearCanvas();
    if (zones.length) {
        for (var i =0; i < zones.length; i++) {
            drawPoly(zones[i].ZonePoints,zones[i].Selected);
            ctx_zones.drawImage(canvas_draw,0,0);
        }
    }
    ctx_draw.clearRect(0, 0, canvas_draw.width, canvas_draw.height);
}
function clearCanvas() {
    ctx_zones.clearRect(0, 0, canvas_zones.width, canvas_zones.height);
    ctx_draw.clearRect(0, 0, canvas_draw.width, canvas_draw.height);
    stopdraw(0);
}
function stopdraw(apply) {
  $("#checkboxAddZone").prop('checked', false);
  if (apply == 0) {
    polybegin=false;
    drawnpoly = [];
    ctx_draw.clearRect(0, 0, canvas_draw.width, canvas_draw.height);
  }
  cb_zone_Clicked();
}

function openImage() {
  imageObj.src = "/static/openspace.png";
}
function onFileSelected(evt) {
  var selectedFile = evt.target.files[0];
  var reader = new FileReader();
  reader.onload = function(evt) {
    imageObj.src = evt.target.result;
  };

  reader.readAsDataURL(selectedFile);
}

function addZone() {
  let prop = new ZoneProperties("Zone" + (zones.length+1),imageObj.width,imageObj.height);
  let newzone = new Zone(prop,drawnpoly);
  zones.push(newzone);
  drawnpoly = [];
  $("#selectZone").append("<option>"+prop.Name+"</option>");
  $("#selectZone option:last").prop("selected", true);
  selectedzonechanged();
}
function deleteZone() {
  zones.splice($("#selectZone option:selected").index(),1);
  $("#selectZone option:selected").remove();
  selectedzonechanged();
  drawAll();
}
function deleteAllZones() {
  $("#selectZone").empty();
  zones = [];
  selectedzonechanged();
  drawAll();
}

function cb_zone_Clicked() {
  if($("#checkboxAddZone").prop('checked')) {
    polybegin=true;
    drawnpoly = [];
    $("#btncanceldraw").show();
  }
  else {
    $("#btncanceldraw").hide();
    if (polybegin) {
      polybegin=false;
      if (drawnpoly.length>2) {
        addZone();
      }
    }
  }
}
function selectedzonechanged() {
    var ind = $("#selectZone option:selected").index();
    for (var i =0; i < zones.length; i++) {
        zones[i].Selected = false;
        if (i == ind) zones[i].Selected = true;
    }
    if (ind>-1)  showproperties(true);
    else showproperties(false);
  drawAll();
}

function showproperties(show) {
  if (show) {
    var ind = $("#selectZone option:selected").index();
    $("#divzoneprop").show();
    $("#selectType").val(zones[ind].Properties.Type);
    $("#txtname").val(zones[ind].Properties.Name);
  }
  else {
    $("#divzoneprop").hide();
  }
}
function updateproperties() {
  var ind = $("#selectZone option:selected").index();
  zones[ind].Properties.Type = $("#selectType option:selected").index()+1;
  zones[ind].Properties.Name = $("#txtname").val();
  $("#selectZone option:selected").text($("#txtname").val());
}

function saveConfig() {

}
