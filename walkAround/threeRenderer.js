
function updateScene(lat, lon, alt, pitch, roll, yaw) {
  camera.position.set(lon, lat, alt);
  camera.rotation.set(pitch, roll, yaw);
  gridHelper.position.set(lon, lat, 0);
  axes.position.set(lon, lat, 1);
  renderer.render(scene, camera);
}

function init() {
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight,01, 2000);
  camera.rotation.order = 'ZXY';
  scene = new THREE.Scene();
  renderer = new THREE.WebGLRenderer();

  //gridlines
  gridHelper = new THREE.GridHelper( 200, 5 );
  gridHelper.rotation.x = 3.14/2.0;
  scene.add( gridHelper );

  //axes
  axes = new THREE.AxisHelper(50);
  scene.add(axes);

  renderer.setSize(window.innerWidth, window.innerHeight);
  container.appendChild(renderer.domElement);

  objectInitializer();
}

function objectInitializer() {
  for (i = 0; i < objectList.length; i++){
    loadModel(objectList[i]['filename'], objectList[i]['latitude'], objectList[i]['longitude'], objectList[i]['altitude'], .75, objectList[i]['x_rot'], objectList[i]['y_rot'], objectList[i]['z_rot']);
  }
}

function loadModel(daeFile, x,y,z, scale, rotationX, rotationY, rotationZ) {
  var loader = new THREE.ColladaLoader();
  loader.options.convertUpAxis = true;
  loader.load(daeFile, function(collada) {
    //upload each object
    var object = collada.scene;
    object.scale.set(scale,scale,scale);
    object.updateMatrix();
    object.position.set(y,x,z);
    object.rotation.set(rotationX,rotationY,rotationZ);
    scene.add(object);

    //give each object directional light
    var directionalLight = new THREE.DirectionalLight( 0xffffff, 0.2 );
    directionalLight.position.set( x, y ,z);
    scene.add( directionalLight );
  });
}
