
function updateScene(lat, lon, alt, pitch, roll, yaw) {
  camera.position.set(lon, lat, alt);
  camera.rotation.set(pitch, roll, yaw, 'ZXY');
  gridHelper.position.set(lon, lat, 100);
  axes.position.set(lon, lat, 100);
  renderer.render(scene, camera);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function render() {
  requestAnimationFrame(render);
  THREE.AnimationHandler.update(clock.getDelta());
  renderer.render(scene, camera);
}

function init() {
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 20000);
  scene = new THREE.Scene();
  renderer = new THREE.WebGLRenderer();
  clock = new THREE.Clock();
  particleLight = new THREE.Mesh(new THREE.SphereGeometry(8, 8, 8), new THREE.MeshBasicMaterial({color: 0x1ad9e0}));

  scene.add(particleLight);

  //gridlines
  gridHelper = new THREE.GridHelper( 200, 5 );
  gridHelper.rotation.x = Math.PI/2;
  scene.add( gridHelper );

  //axes
  axes = new THREE.AxisHelper(25);
  scene.add(axes);

  var pointLight = new THREE.PointLight(0x1ad9e0, 2);
  particleLight.add(pointLight);

  renderer.setSize(window.innerWidth, window.innerHeight);

  container.appendChild(renderer.domElement);
  // window.addEventListener('resize', onWindowResize, false);
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
    // object.name = daeFile;
    object.updateMatrix();
    object.position.set(y,x,z);
    console.log(object.position);
  //  object.matrixAutoUpdate = false;
    object.rotation.set(rotationX,rotationY,rotationZ);
    scene.add(object);
    //give each object directional light
    var directionalLight = new THREE.DirectionalLight( 0xffffff, 0.2 );
    directionalLight.position.set( x, y ,z); 
    scene.add( directionalLight );
    
  });
} 
