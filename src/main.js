import * as THREE from "three";

const LANE_X = [-3, 0, 3];
const ROAD_BOUNDS_Y = 12;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x08141f);

const camera = new THREE.OrthographicCamera(-8, 8, 8, -8, 0.1, 100);
camera.position.set(0, 0, 20);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
directionalLight.position.set(0, 8, 14);
scene.add(directionalLight);

const road = new THREE.Mesh(
  new THREE.PlaneGeometry(10, ROAD_BOUNDS_Y * 2 + 2),
  new THREE.MeshPhongMaterial({ color: 0x32373b })
);
scene.add(road);

const shoulderMaterial = new THREE.MeshPhongMaterial({ color: 0x8f999f });
const leftShoulder = new THREE.Mesh(new THREE.PlaneGeometry(0.45, 26), shoulderMaterial);
leftShoulder.position.x = -5.2;
leftShoulder.position.z = 0.01;
scene.add(leftShoulder);

const rightShoulder = leftShoulder.clone();
rightShoulder.position.x = 5.2;
scene.add(rightShoulder);

const laneMarkers = [];
const laneMarkerGeometry = new THREE.PlaneGeometry(0.25, 1.8);
const laneMarkerMaterial = new THREE.MeshBasicMaterial({ color: 0xf8f7de });
const markerColumns = [-1.5, 1.5];
for (const columnX of markerColumns) {
  for (let y = -12; y <= 12; y += 3.2) {
    const marker = new THREE.Mesh(laneMarkerGeometry, laneMarkerMaterial);
    marker.position.set(columnX, y, 0.02);
    laneMarkers.push(marker);
    scene.add(marker);
  }
}

const scoreEl = document.getElementById("score");
const statusEl = document.getElementById("status");

function buildCar(color) {
  const group = new THREE.Group();

  const body = new THREE.Mesh(
    new THREE.BoxGeometry(1.6, 2.8, 0.6),
    new THREE.MeshPhongMaterial({ color })
  );
  body.position.z = 0.35;
  group.add(body);

  const cabin = new THREE.Mesh(
    new THREE.BoxGeometry(1.1, 1.2, 0.45),
    new THREE.MeshPhongMaterial({ color: 0xe8f0ff })
  );
  cabin.position.set(0, 0.25, 0.85);
  group.add(cabin);

  const bumper = new THREE.Mesh(
    new THREE.BoxGeometry(1.45, 0.3, 0.14),
    new THREE.MeshPhongMaterial({ color: 0x111111 })
  );
  bumper.position.set(0, 1.35, 0.25);
  group.add(bumper);

  const rearBumper = bumper.clone();
  rearBumper.position.y = -1.35;
  group.add(rearBumper);

  return group;
}

const player = buildCar(0x1d9bf0);
scene.add(player);

let playerLane = 1;
let playerTargetX = LANE_X[playerLane];
player.position.set(playerTargetX, -8.2, 0);

const obstacles = [];
const obstacleColors = [0xef4444, 0xf97316, 0xa855f7, 0x22c55e, 0xfacc15];
let spawnCooldown = 0.8;
let spawnTimer = 0;
let score = 0;
let gameOver = false;

const playerBox = new THREE.Box3();
const obstacleBox = new THREE.Box3();
const clock = new THREE.Clock();

function randomItem(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function spawnObstacle() {
  const obstacle = buildCar(randomItem(obstacleColors));
  const lane = Math.floor(Math.random() * LANE_X.length);
  obstacle.position.set(LANE_X[lane], ROAD_BOUNDS_Y + 2.5, 0);
  obstacle.userData.speed = 7 + Math.random() * 3 + Math.min(score * 0.02, 3);
  obstacles.push(obstacle);
  scene.add(obstacle);
}

function clearObstacles() {
  for (const obstacle of obstacles) {
    scene.remove(obstacle);
  }
  obstacles.length = 0;
}

function resetGame() {
  clearObstacles();
  playerLane = 1;
  playerTargetX = LANE_X[playerLane];
  player.position.set(playerTargetX, -8.2, 0);
  score = 0;
  spawnTimer = 0;
  spawnCooldown = 0.8;
  gameOver = false;
  scoreEl.textContent = "Score: 0";
  statusEl.textContent = "Use ← and → to dodge traffic";
}

function endGame() {
  gameOver = true;
  statusEl.textContent = "Crash! Press R or Space to restart";
}

function updateCameraBounds() {
  const aspect = window.innerWidth / window.innerHeight;
  const halfHeight = 8;
  camera.top = halfHeight;
  camera.bottom = -halfHeight;
  camera.left = -halfHeight * aspect;
  camera.right = halfHeight * aspect;
  camera.updateProjectionMatrix();
}

window.addEventListener("resize", () => {
  updateCameraBounds();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

window.addEventListener("keydown", (event) => {
  if (gameOver && (event.code === "Space" || event.code === "KeyR")) {
    resetGame();
    return;
  }

  if (gameOver) {
    return;
  }

  if (event.code === "ArrowLeft" || event.code === "KeyA") {
    playerLane = Math.max(0, playerLane - 1);
    playerTargetX = LANE_X[playerLane];
  }
  if (event.code === "ArrowRight" || event.code === "KeyD") {
    playerLane = Math.min(LANE_X.length - 1, playerLane + 1);
    playerTargetX = LANE_X[playerLane];
  }
});

updateCameraBounds();

function animate() {
  const delta = Math.min(clock.getDelta(), 0.05);

  for (const marker of laneMarkers) {
    marker.position.y -= delta * 7;
    if (marker.position.y < -ROAD_BOUNDS_Y - 1) {
      marker.position.y += ROAD_BOUNDS_Y * 2 + 2;
    }
  }

  if (!gameOver) {
    const targetOffset = playerTargetX - player.position.x;
    player.position.x += targetOffset * Math.min(1, delta * 14);

    spawnTimer -= delta;
    if (spawnTimer <= 0) {
      spawnObstacle();
      spawnCooldown = Math.max(0.38, spawnCooldown - 0.01);
      spawnTimer = spawnCooldown;
    }

    playerBox.setFromObject(player);

    for (let i = obstacles.length - 1; i >= 0; i -= 1) {
      const obstacle = obstacles[i];
      obstacle.position.y -= obstacle.userData.speed * delta;

      obstacleBox.setFromObject(obstacle);
      if (playerBox.intersectsBox(obstacleBox)) {
        endGame();
        break;
      }

      if (obstacle.position.y < -ROAD_BOUNDS_Y - 4) {
        scene.remove(obstacle);
        obstacles.splice(i, 1);
      }
    }

    score += delta * 12;
    scoreEl.textContent = `Score: ${Math.floor(score)}`;
  }

  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

animate();
