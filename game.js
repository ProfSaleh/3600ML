"use strict";

const scoreEl = document.getElementById("score");
const gameOverEl = document.getElementById("game-over");
const finalScoreEl = document.getElementById("final-score");
const restartBtn = document.getElementById("restart-btn");

const ROAD_WIDTH = 8.4;
const ROAD_HEIGHT = 20;
const PLAYER_Y = -6.5;
const LANE_CENTERS = [-2.8, 0, 2.8];
const PLAYER_SIZE = { width: 1.25, height: 2.25 };
const ENEMY_SIZE = { width: 1.2, height: 2.2 };

const ENEMY_COLORS = [0xff5e5e, 0xffb347, 0x57d6a4, 0xc58cff, 0xfff16b];

const state = {
  currentLane: 1,
  targetX: LANE_CENTERS[1],
  score: 0,
  elapsed: 0,
  spawnTimer: 0,
  spawnInterval: 1.05,
  isGameOver: false,
};

const enemies = [];
const laneMarkers = [];

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05070d);

const camera = new THREE.OrthographicCamera(-6, 6, 9, -9, 0.1, 100);
camera.position.set(0, 0, 20);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
scene.add(ambientLight);

const keyLight = new THREE.DirectionalLight(0xffffff, 0.9);
keyLight.position.set(2, 4, 9);
scene.add(keyLight);

const road = new THREE.Mesh(
  new THREE.PlaneGeometry(ROAD_WIDTH, ROAD_HEIGHT),
  new THREE.MeshPhongMaterial({ color: 0x1d232d })
);
scene.add(road);

const shoulderGeometry = new THREE.PlaneGeometry(0.75, ROAD_HEIGHT);
const shoulderMaterial = new THREE.MeshPhongMaterial({ color: 0x2f3744 });
const leftShoulder = new THREE.Mesh(shoulderGeometry, shoulderMaterial);
leftShoulder.position.set(-ROAD_WIDTH / 2 - 0.4, 0, 0);
scene.add(leftShoulder);
const rightShoulder = leftShoulder.clone();
rightShoulder.position.x = ROAD_WIDTH / 2 + 0.4;
scene.add(rightShoulder);

const dividerX = [(LANE_CENTERS[0] + LANE_CENTERS[1]) / 2, (LANE_CENTERS[1] + LANE_CENTERS[2]) / 2];
const markerGeometry = new THREE.PlaneGeometry(0.2, 1.1);
const markerMaterial = new THREE.MeshPhongMaterial({ color: 0xf9fbff });
const markerCount = 16;
for (let lane = 0; lane < dividerX.length; lane += 1) {
  for (let i = 0; i < markerCount; i += 1) {
    const marker = new THREE.Mesh(markerGeometry, markerMaterial);
    marker.position.set(dividerX[lane], -ROAD_HEIGHT / 2 + i * 1.5, 0.01);
    laneMarkers.push(marker);
    scene.add(marker);
  }
}

function createCar(color) {
  const car = new THREE.Group();

  const body = new THREE.Mesh(
    new THREE.BoxGeometry(PLAYER_SIZE.width, PLAYER_SIZE.height, 0.75),
    new THREE.MeshPhongMaterial({ color })
  );
  body.position.z = 0.38;
  car.add(body);

  const roof = new THREE.Mesh(
    new THREE.BoxGeometry(0.85, 1.15, 0.65),
    new THREE.MeshPhongMaterial({ color: 0xdbe8ff })
  );
  roof.position.set(0, 0.15, 0.95);
  car.add(roof);

  const wheelGeometry = new THREE.BoxGeometry(0.22, 0.5, 0.32);
  const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x111217 });
  const wheelOffsets = [
    [-0.66, -0.72],
    [0.66, -0.72],
    [-0.66, 0.72],
    [0.66, 0.72],
  ];

  for (const [x, y] of wheelOffsets) {
    const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
    wheel.position.set(x, y, 0.2);
    car.add(wheel);
  }

  return car;
}

const player = createCar(0x4a8dff);
player.position.set(LANE_CENTERS[state.currentLane], PLAYER_Y, 0.2);
scene.add(player);

function spawnEnemy() {
  let lane = Math.floor(Math.random() * LANE_CENTERS.length);
  let tries = 0;

  // Avoid spawning directly on top of another car in the same lane.
  while (tries < 4) {
    const blocked = enemies.some((enemy) => enemy.lane === lane && enemy.mesh.position.y > 5.8);
    if (!blocked) break;
    lane = (lane + 1) % LANE_CENTERS.length;
    tries += 1;
  }

  const enemy = {
    lane,
    speed: 6.8 + Math.random() * 1.8 + state.elapsed * 0.2,
    mesh: createCar(ENEMY_COLORS[Math.floor(Math.random() * ENEMY_COLORS.length)]),
  };

  enemy.mesh.position.set(LANE_CENTERS[lane], ROAD_HEIGHT / 2 + 1.8, 0.2);
  enemies.push(enemy);
  scene.add(enemy.mesh);
}

function removeEnemy(index) {
  scene.remove(enemies[index].mesh);
  enemies.splice(index, 1);
}

function updateScoreDisplay() {
  scoreEl.textContent = `Score: ${Math.floor(state.score)}`;
}

function updateLaneMarkers(delta) {
  const markerSpeed = 8.6 + state.elapsed * 0.7;
  for (const marker of laneMarkers) {
    marker.position.y -= markerSpeed * delta;
    if (marker.position.y < -ROAD_HEIGHT / 2 - 0.9) {
      marker.position.y += ROAD_HEIGHT + 2.4;
    }
  }
}

function intersects(a, b) {
  return Math.abs(a.x - b.x) < a.hw + b.hw && Math.abs(a.y - b.y) < a.hh + b.hh;
}

function endGame() {
  state.isGameOver = true;
  finalScoreEl.textContent = `Score: ${Math.floor(state.score)}`;
  gameOverEl.classList.remove("hidden");
}

function resetGame() {
  for (let i = enemies.length - 1; i >= 0; i -= 1) {
    removeEnemy(i);
  }

  state.currentLane = 1;
  state.targetX = LANE_CENTERS[1];
  state.score = 0;
  state.elapsed = 0;
  state.spawnTimer = 0;
  state.spawnInterval = 1.05;
  state.isGameOver = false;
  player.position.x = LANE_CENTERS[state.currentLane];
  updateScoreDisplay();
  gameOverEl.classList.add("hidden");
}

function shiftLane(direction) {
  if (state.isGameOver) return;
  const nextLane = THREE.MathUtils.clamp(state.currentLane + direction, 0, LANE_CENTERS.length - 1);
  if (nextLane !== state.currentLane) {
    state.currentLane = nextLane;
    state.targetX = LANE_CENTERS[nextLane];
  }
}

function onKeyDown(event) {
  if (event.key === "ArrowLeft" || event.key === "a" || event.key === "A") {
    if (!event.repeat) shiftLane(-1);
  } else if (event.key === "ArrowRight" || event.key === "d" || event.key === "D") {
    if (!event.repeat) shiftLane(1);
  } else if (event.key === "Enter" && state.isGameOver) {
    resetGame();
  }
}

window.addEventListener("keydown", onKeyDown);
restartBtn.addEventListener("click", resetGame);

function resize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height);

  const viewHeight = 18;
  const viewWidth = Math.max(11, viewHeight * (width / height));
  camera.left = -viewWidth / 2;
  camera.right = viewWidth / 2;
  camera.top = viewHeight / 2;
  camera.bottom = -viewHeight / 2;
  camera.updateProjectionMatrix();
}

window.addEventListener("resize", resize);
resize();
updateScoreDisplay();

const clock = new THREE.Clock();

function updateGame(delta) {
  state.elapsed += delta;
  state.score += delta * 13.5;
  state.spawnInterval = Math.max(0.38, 1.05 - state.elapsed * 0.02);
  state.spawnTimer += delta;

  if (state.spawnTimer >= state.spawnInterval) {
    state.spawnTimer = 0;
    spawnEnemy();
  }

  player.position.x = THREE.MathUtils.damp(player.position.x, state.targetX, 16, delta);
  updateLaneMarkers(delta);

  const playerBounds = {
    x: player.position.x,
    y: player.position.y,
    hw: PLAYER_SIZE.width * 0.45,
    hh: PLAYER_SIZE.height * 0.44,
  };

  for (let i = enemies.length - 1; i >= 0; i -= 1) {
    const enemy = enemies[i];
    enemy.mesh.position.y -= enemy.speed * delta;

    if (enemy.mesh.position.y < -ROAD_HEIGHT / 2 - 2.6) {
      removeEnemy(i);
      continue;
    }

    const enemyBounds = {
      x: enemy.mesh.position.x,
      y: enemy.mesh.position.y,
      hw: ENEMY_SIZE.width * 0.45,
      hh: ENEMY_SIZE.height * 0.44,
    };

    if (intersects(playerBounds, enemyBounds)) {
      endGame();
      break;
    }
  }

  updateScoreDisplay();
}

function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.05);
  if (!state.isGameOver) updateGame(delta);
  renderer.render(scene, camera);
}

animate();
