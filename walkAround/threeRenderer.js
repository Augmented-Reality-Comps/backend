
window.onload = function() {
  console.log("loaded");
}

function setLocation(latitude, longitude, altitude, yaw, pitch, roll) {
  camera.position = (latitude, longitude, altitude);
  camera.rotation = (yaw, pitch, roll);
}

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

function getValues(){
  console.log(camera.position.x, camera.position.y, camera.position.z, camera.rotation.x, camera.rotation.y, camera.rotation.z);
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
