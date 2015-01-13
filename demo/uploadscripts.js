var uploaded_file;
var files;
if (window.File && window.FileReader && window.FileList) {
  // Great success! All the File APIs are supported.
} else {
  alert('The File APIs are not fully supported in this browser.');
}

var uploaded_file;

navigator.geolocation.getCurrentPosition(init_map);

function init_map(position) {
  var myOptions = {
    zoom: 16,
    center: new google.maps.LatLng(position.coords.latitude.toPrecision(8), position.coords.longitude.toPrecision(8)),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  $('#lat').val(position.coords.latitude.toPrecision(8));
  $('#long').val(position.coords.longitude.toPrecision(8));
  map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);
  google.maps.event.addListener(
    map, 'click',
    function(event) {
      $('#lat').val(event.latLng.lat().toPrecision(8));
      $('#long').val(event.latLng.lng().toPrecision(8));
    }
  );
}

function testValidDAE() {
  uploaded_file = $('#collada').get(0).files[0];
  console.log(uploaded_file);
  //alert("changed File");
  //var parser = new DOMParser();
  //var doc = parser.parseFromString( fileAsString, "application/xml");
}

function handleFileSelect(evt) {
  evt.stopPropagation();
  evt.preventDefault();

  files = evt.dataTransfer.files; // FileList object.
  uploaded_file = files[0];

  var reader = new FileReader();
  reader.readAsText(file);

  // files is a FileList of File objects. List some properties.
  var output = [];
  for (var i = 0, f; f = files[i]; i++) {
    output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
    f.size, ' bytes, last modified: ',
    f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
    '</li>');
  }
  document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

function handleDragOver(evt) {
  evt.stopPropagation();
  evt.preventDefault();
  evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

//Checks that file is valid COLLADA file before syncing with database
function checkValidDAE(file) {
  //<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
}

//Stores coordinates + object into database
function syncObjectDatabase() {
  //
}

function setDropListeners() {
  // Setup the dnd listeners.
  var dropZone = document.getElementById('drop_zone');
  dropZone.addEventListener('dragover', handleDragOver, false);
  dropZone.addEventListener('drop', handleFileSelect, false);
}

window.onload = setDropListeners;
