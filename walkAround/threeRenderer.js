function getLocation() {
  return [camera.position.x, camera.position.y, camera.position.z]
}

function getAngle() {
  return [camera.rotation.x, camera.rotation.y, camera.rotation.z]
}

function updateScene(lat, long, alt, pitch, roll, yaw) {
  container = document.getElementById("scene");

  camera.position.set(lat, long, alt)
  camera.rotation.set(pitch, roll, yaw);

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
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 2000);
  scene = new THREE.Scene();
  renderer = new THREE.WebGLRenderer();
  clock = new THREE.Clock();
  particleLight = new THREE.Mesh(new THREE.SphereGeometry(8, 8, 8), new THREE.MeshBasicMaterial({color: 0xff0000}));

  scene.add(particleLight);
  scene.add(new THREE.AmbientLight(0x888888));

  var pointLight = new THREE.PointLight(0xff0000, 2);
  particleLight.add(pointLight);

  renderer.setSize(window.innerWidth, window.innerHeight);

  container.appendChild(renderer.domElement);
  window.addEventListener('resize', onWindowResize, false);
}

function objectInitializer() {
  for (i = 0; i < objectList.length; i++){
    loadModel(objectList[i]['filename'], objectList[i]['filename'], objectList[i]['latitude'], objectList[i]['longitude'], objectList[i]['altitude'], 1);
  }
}

function loadModel(daeFile, name, x,y,z, scale) {
  var loader = new THREE.ColladaLoader();
  loader.options.convertUpAxis = true;
  loader.load(daeFile, function(collada) {
    var object = collada.scene;
    object.scale.set(scale,scale,scale);
    object.name = name;
    object.updateMatrix();
    object.position.set(x,y,z);
    scene.add(object);
  });
}

//Camera view button methods
function changeX(distance) {
  camera.position.x += distance;
}

function changeY(distance) {
  camera.position.y += distance;
}

function changeZ(distance) {
  camera.position.z += distance;
}

function anglePitch(radians) {
  camera.rotation.x += radians
}

function angleRoll(radians) {
  camera.rotation.y += radians
}

function angleYaw(radians) {
  camera.rotation.z += radians
}

