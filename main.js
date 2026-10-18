// 3D Spider-Man City Explorer Sandbox
// Powered by Three.js

const container = document.getElementById('canvas-container');

// --- 1. SETUP THREE.JS SCENE ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.FogExp2(0x0a0a14, 0.007);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // cap at 2x — no visible gain above that
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

// --- 2. LIGHTING ---
const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
scene.add(ambientLight);

const hemiLight = new THREE.HemisphereLight(0x2979ff, 0xff1744, 0.3);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xffe0b2, 0.8);
dirLight.position.set(100, 150, 50);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 1024;  // was 2048 — halves shadow cost
dirLight.shadow.mapSize.height = 1024;
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 500;
const d = 150;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
scene.add(dirLight);

// --- 3. PROCEDURAL TEXTURES ---
// Procedural Building Window Texture
function createBuildingTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');

    // Dark building background
    ctx.fillStyle = '#15151c';
    ctx.fillRect(0, 0, 128, 128);

    // Windows
    const rows = 8;
    const cols = 4;
    const wWidth = 16;
    const wHeight = 8;
    const padX = 12;
    const padY = 6;

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            // Randomly turn on/off lights
            const rand = Math.random();
            if (rand > 0.4) {
                ctx.fillStyle = rand > 0.85 ? '#ffeb3b' : '#ff9800'; // Orange/Yellow lights
            } else {
                ctx.fillStyle = '#0a0a0f'; // Dark window
            }
            ctx.fillRect(
                padX + c * (wWidth + padX),
                padY + r * (wHeight + padY),
                wWidth,
                wHeight
            );
        }
    }

    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    return texture;
}

const buildingTexture = createBuildingTexture();

// --- 4. GENERATE CITY ENVIRONMENT ---
const groundSize = 1000;
const groundGeo = new THREE.PlaneGeometry(groundSize, groundSize);
const groundMat = new THREE.MeshStandardMaterial({ 
    color: 0x111116, 
    roughness: 0.8 
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Procedural Roads
const roadMaterial = new THREE.MeshStandardMaterial({ color: 0x08080a, roughness: 0.9 });
const roads = [];
const gridSpacing = 80;

for (let i = -groundSize/2; i <= groundSize/2; i += gridSpacing) {
    // East-West Roads
    const roadEW = new THREE.Mesh(new THREE.PlaneGeometry(groundSize, 12), roadMaterial);
    roadEW.rotation.x = -Math.PI / 2;
    roadEW.position.set(0, 0.01, i);
    roadEW.receiveShadow = true;
    scene.add(roadEW);

    // North-South Roads
    const roadNS = new THREE.Mesh(new THREE.PlaneGeometry(12, groundSize), roadMaterial);
    roadNS.rotation.x = -Math.PI / 2;
    roadNS.position.set(i, 0.01, 0);
    roadNS.receiveShadow = true;
    scene.add(roadNS);
}

// Generate Buildings
const buildings = [];
const buildingGeometry = new THREE.BoxGeometry(1, 1, 1);

// Generate buildings in grid blocks
for (let x = -groundSize/2 + 20; x < groundSize/2 - 20; x += gridSpacing) {
    for (let z = -groundSize/2 + 20; z < groundSize/2 - 20; z += gridSpacing) {
        // Place multiple buildings per block
        const bCount = 4 + Math.floor(Math.random() * 4);
        for (let b = 0; b < bCount; b++) {
            const bWidth = 15 + Math.random() * 15;
            const bDepth = 15 + Math.random() * 15;
            const bHeight = 40 + Math.random() * 100;

            // Offset building inside the grid cell
            const offsetX = (Math.random() - 0.5) * 40;
            const offsetZ = (Math.random() - 0.5) * 40;

            // Prevent buildings directly on roads
            const posX = x + offsetX;
            const posZ = z + offsetZ;
            if (Math.abs(posX % gridSpacing) < 12 || Math.abs(posZ % gridSpacing) < 12) continue;

            const mat = new THREE.MeshStandardMaterial({
                map: buildingTexture,
                roughness: 0.5,
                metalness: 0.1
            });
            // Repeat texture according to building scale
            mat.map.repeat.set(bWidth / 15, bHeight / 15);

            const building = new THREE.Mesh(buildingGeometry, mat);
            building.scale.set(bWidth, bHeight, bDepth);
            building.position.set(posX, bHeight / 2, posZ);
            // Only cast/receive shadows for buildings near centre — big perf win
            const distFromCenter = Math.sqrt(posX * posX + posZ * posZ);
            building.castShadow = distFromCenter < 200;
            building.receiveShadow = distFromCenter < 200;
            
            // Store bounding box data for collision detection
            building.userData = {
                halfWidth: bWidth / 2,
                halfHeight: bHeight / 2,
                halfDepth: bDepth / 2,
                minX: posX - bWidth / 2,
                maxX: posX + bWidth / 2,
                minZ: posZ - bDepth / 2,
                maxZ: posZ + bDepth / 2,
                height: bHeight
            };

            scene.add(building);
            buildings.push(building);
        }
    }
}

// --- 4.5 GENERATE CHEERLEADERS & CITIZENS ---
const cheerleaders = [];
const cheerMat1 = new THREE.MeshStandardMaterial({ color: 0xff4081, roughness: 0.5 }); // Pink outfit
const cheerMat2 = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.5 }); // White outfit
const skinMat = new THREE.MeshStandardMaterial({ color: 0xffd54f, roughness: 0.6 }); // Gold/Yellow skin

function spawnCheerleader(x, z) {
    const group = new THREE.Group();
    group.position.set(x, 0.8, z);

    // Skirt/Lower Torso (Cone)
    const skirt = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 8), cheerMat1);
    skirt.position.y = 0.2;
    skirt.castShadow = true;
    group.add(skirt);

    // Top Torso (Cylinder)
    const top = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.4, 8), cheerMat2);
    top.position.y = 0.6;
    top.castShadow = true;
    group.add(top);

    // Head
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 12, 12), skinMat);
    head.position.y = 0.95;
    head.castShadow = true;
    group.add(head);

    // Pom Poms (Pink spheres)
    const pomL = new THREE.Mesh(new THREE.SphereGeometry(0.15, 8, 8), cheerMat1);
    pomL.position.set(0.35, 0.6, 0.1);
    group.add(pomL);

    const pomR = new THREE.Mesh(new THREE.SphereGeometry(0.15, 8, 8), cheerMat1);
    pomR.position.set(-0.35, 0.6, 0.1);
    group.add(pomR);

    scene.add(group);
    cheerleaders.push({
        mesh: group,
        pomL: pomL,
        pomR: pomR,
        phase: Math.random() * Math.PI * 2,
        speed: 5 + Math.random() * 5,
        initialY: 0.8
    });
}

// Spawn cheerleaders in groups near the road intersections
for (let i = -groundSize/2 + 80; i < groundSize/2; i += gridSpacing) {
    for (let j = -groundSize/2 + 80; j < groundSize/2; j += gridSpacing) {
        // Spawn a small group at corners of intersections
        spawnCheerleader(i - 8, j - 8);
        spawnCheerleader(i + 8, j - 8);
        spawnCheerleader(i - 8, j + 8);
        spawnCheerleader(i + 8, j + 8);
    }
}

// --- 5. CREATE PLAYER (SPIDER-MAN STYLE HERO) ---
const playerGroup = new THREE.Group();
scene.add(playerGroup);

// Materials
const redMat = new THREE.MeshStandardMaterial({ color: 0xd50000, roughness: 0.5 });
const blueMat = new THREE.MeshStandardMaterial({ color: 0x0d47a1, roughness: 0.5 });
const whiteMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.2 });

// Torso (Red and Blue)
const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.4, 1.6, 8), redMat);
torso.position.y = 0.8;
torso.castShadow = true;
playerGroup.add(torso);

const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.4, 8), blueMat);
belt.position.y = 0.3;
belt.castShadow = true;
playerGroup.add(belt);

// Head (Red with White Eyes)
const head = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 16), redMat);
head.position.y = 1.9;
head.castShadow = true;
playerGroup.add(head);

// Eyes
const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), whiteMat);
eyeL.scale.set(1.5, 1, 0.3);
eyeL.position.set(0.18, 1.95, 0.42);
eyeL.rotation.y = 0.3;
playerGroup.add(eyeL);

const eyeR = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), whiteMat);
eyeR.scale.set(1.5, 1, 0.3);
eyeR.position.set(-0.18, 1.95, 0.42);
eyeR.rotation.y = -0.3;
playerGroup.add(eyeR);

// Limbs
const armL = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.15, 1.2, 8), redMat);
armL.position.set(0.85, 1.0, 0);
armL.rotation.z = -0.2;
armL.castShadow = true;
playerGroup.add(armL);

const armR = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.15, 1.2, 8), redMat);
armR.position.set(-0.85, 1.0, 0);
armR.rotation.z = 0.2;
armR.castShadow = true;
playerGroup.add(armR);

const legL = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.18, 1.4, 8), blueMat);
legL.position.set(0.35, -0.4, 0);
legL.castShadow = true;
playerGroup.add(legL);

const legR = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.18, 1.4, 8), blueMat);
legR.position.set(-0.35, -0.4, 0);
legR.castShadow = true;
playerGroup.add(legR);

// Set player initial physics state
const player = {
    pos: new THREE.Vector3(0, 1.1, 0),
    vel: new THREE.Vector3(0, 0, 0),
    radius: 1.0,
    height: 2.5,
    onGround: true,
    moveSpeed: 0.25,
    rotation: 0,
    swinging: false,
    webAnchor: null,
    ropeLength: 0
};
playerGroup.position.copy(player.pos);

// Web Visual Line
const webMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
const webGeometry = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
const webLine = new THREE.Line(webGeometry, webMaterial);
webLine.visible = false;
scene.add(webLine);

// --- 6. CONTROLS AND INPUT HANDLING ---
const keys = { w: false, a: false, s: false, d: false, space: false };

window.addEventListener('keydown', (e) => {
    switch (e.code) {
        case 'KeyW': keys.w = true; break;
        case 'KeyA': keys.a = true; break;
        case 'KeyS': keys.s = true; break;
        case 'KeyD': keys.d = true; break;
        case 'Space': 
            if (!keys.space) startSwing();
            keys.space = true; 
            break;
    }
});

window.addEventListener('keyup', (e) => {
    switch (e.code) {
        case 'KeyW': keys.w = false; break;
        case 'KeyA': keys.a = false; break;
        case 'KeyS': keys.s = false; break;
        case 'KeyD': keys.d = false; break;
        case 'Space': 
            keys.space = false; 
            endSwing();
            break;
    }
});

// Camera Mouse Look Controls
let theta = 0; // Horizontal camera angle
let phi = Math.PI / 4; // Vertical camera angle
const cameraDistance = 15;

let isMouseDown = false;
let previousMousePosition = { x: 0, y: 0 };

window.addEventListener('mousedown', (e) => {
    isMouseDown = true;
    previousMousePosition = { x: e.clientX, y: e.clientY };
});

window.addEventListener('mouseup', () => {
    isMouseDown = false;
});

window.addEventListener('mousemove', (e) => {
    if (!isMouseDown) return;

    const deltaX = e.clientX - previousMousePosition.x;
    const deltaY = e.clientY - previousMousePosition.y;

    theta -= deltaX * 0.005;
    phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.1, phi + deltaY * 0.005));

    previousMousePosition = { x: e.clientX, y: e.clientY };
});

// Touch controls for mobile
window.addEventListener('touchstart', (e) => {
    isMouseDown = true;
    previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
});
window.addEventListener('touchmove', (e) => {
    if (!isMouseDown) return;
    const deltaX = e.touches[0].clientX - previousMousePosition.x;
    const deltaY = e.touches[0].clientY - previousMousePosition.y;

    theta -= deltaX * 0.007;
    phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.1, phi + deltaY * 0.007));

    previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
});
window.addEventListener('touchend', () => {
    isMouseDown = false;
});

// --- 7. GAME MECHANICS & SWINGING PHYSICS ---

function startSwing() {
    if (player.swinging) return;

    // Find the closest building structure above the player
    let bestAnchor = null;
    let closestDist = Infinity;

    // Direct ray direction (forward and upwards based on camera view)
    const lookDir = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), theta);
    lookDir.y = 1.0; // Angle upwards
    lookDir.normalize();

    // Check potential buildings to attach web
    for (let b of buildings) {
        // Simple bounding height check
        if (b.position.y > player.pos.y) {
            const dist = player.pos.distanceTo(b.position);
            if (dist < 150 && dist < closestDist) {
                // Attach web to building roof/face
                closestDist = dist;
                bestAnchor = new THREE.Vector3(
                    b.position.x + (Math.random() - 0.5) * b.scale.x * 0.5,
                    b.position.y + b.scale.y * 0.5,
                    b.position.z + (Math.random() - 0.5) * b.scale.z * 0.5
                );
            }
        }
    }

    if (bestAnchor) {
        player.swinging = true;
        player.webAnchor = bestAnchor;
        player.ropeLength = player.pos.distanceTo(bestAnchor);
        webLine.visible = true;
    } else {
        // Fallback jump if no buildings nearby
        if (player.onGround) {
            player.vel.y = 8;
            player.onGround = false;
        }
    }
}

function endSwing() {
    if (player.swinging) {
        player.swinging = false;
        player.webAnchor = null;
        webLine.visible = false;
    }
}

// --- 8. COLLISION DETECTION ---
function checkCollisions(newPos) {
    // Ground collision
    if (newPos.y < 1.1) {
        newPos.y = 1.1;
        player.vel.y = 0;
        player.onGround = true;
    }

    // Building collisions (AABB Check)
    for (let b of buildings) {
        const u = b.userData;
        if (
            newPos.x + player.radius > u.minX &&
            newPos.x - player.radius < u.maxX &&
            newPos.z + player.radius > u.minZ &&
            newPos.z - player.radius < u.maxZ &&
            newPos.y - 1.1 < u.height
        ) {
            // Push player back depending on closest axis
            const distMinX = Math.abs((newPos.x + player.radius) - u.minX);
            const distMaxX = Math.abs((newPos.x - player.radius) - u.maxX);
            const distMinZ = Math.abs((newPos.z + player.radius) - u.minZ);
            const distMaxZ = Math.abs((newPos.z - player.radius) - u.maxZ);

            const minDist = Math.min(distMinX, distMaxX, distMinZ, distMaxZ);

            if (minDist === distMinX) newPos.x = u.minX - player.radius;
            else if (minDist === distMaxX) newPos.x = u.maxX + player.radius;
            else if (minDist === distMinZ) newPos.z = u.minZ - player.radius;
            else if (minDist === distMaxZ) newPos.z = u.maxZ + player.radius;
            
            // Cancel horizontal velocity on collision
            player.vel.x = 0;
            player.vel.z = 0;
        }
    }
}

// --- 9. UPDATE AND RENDER LOOP ---
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const dt = Math.min(clock.getDelta(), 0.1); // Cap time delta

    // --- Physics Update ---
    if (player.swinging && player.webAnchor) {
        // Web swinging physics (Pendulum)
        // Gravity force vector
        const gravityForce = new THREE.Vector3(0, -9.8 * 2.0, 0);
        player.vel.addScaledVector(gravityForce, dt);

        // Position prediction
        const nextPos = player.pos.clone().addScaledVector(player.vel, dt);

        // Rope tension vector (pointing toward anchor)
        const toAnchor = new THREE.Vector3().subVectors(player.webAnchor, nextPos);
        const currentDist = toAnchor.length();

        if (currentDist > player.ropeLength) {
            toAnchor.normalize();
            
            // Constrain position to rope length
            const offset = currentDist - player.ropeLength;
            nextPos.addScaledVector(toAnchor, offset);

            // Project velocity onto sphere constraint (remove outward component)
            const velProj = player.vel.dot(toAnchor);
            if (velProj < 0) {
                // Subtract velocity component facing away from anchor
                player.vel.addScaledVector(toAnchor, -velProj);
            }
        }

        player.pos.copy(nextPos);
        
        // Add swing boost using WASD
        const forward = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), theta);
        const right = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), theta);
        
        if (keys.w) player.vel.addScaledVector(forward, 15 * dt);
        if (keys.s) player.vel.addScaledVector(forward, -15 * dt);
        if (keys.a) player.vel.addScaledVector(right, -15 * dt);
        if (keys.d) player.vel.addScaledVector(right, 15 * dt);

    } else {
        // Standard walk / jump controls
        const forward = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), theta);
        const right = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), theta);
        
        const moveDir = new THREE.Vector3();
        if (keys.w) moveDir.add(forward);
        if (keys.s) moveDir.add(forward.clone().negate());
        if (keys.a) moveDir.add(right.clone().negate());
        if (keys.d) moveDir.add(right);

        moveDir.y = 0; // Lock to flat horizontal movement
        moveDir.normalize();

        if (player.onGround) {
            // Decelerate quickly on ground
            player.vel.x += (moveDir.x * player.moveSpeed * 10 - player.vel.x) * 0.15;
            player.vel.z += (moveDir.z * player.moveSpeed * 10 - player.vel.z) * 0.15;
        } else {
            // Air control (less responsive)
            player.vel.x += moveDir.x * player.moveSpeed * 0.5;
            player.vel.z += moveDir.z * player.moveSpeed * 0.5;
            
            // Air friction
            player.vel.x *= 0.99;
            player.vel.z *= 0.99;

            // Gravity
            player.vel.y -= 25 * dt;
        }

        // Apply velocities
        player.pos.addScaledVector(player.vel, dt);
    }

    // Check ground & building collisions
    checkCollisions(player.pos);

    // Apply position to mesh
    playerGroup.position.copy(player.pos);

    // Align player rotation to face movement direction
    if (Math.abs(player.vel.x) > 0.05 || Math.abs(player.vel.z) > 0.05) {
        player.rotation = Math.atan2(player.vel.x, player.vel.z);
        playerGroup.rotation.y = player.rotation;
    }

    // --- Animate Cheerleaders ---
    const time = clock.getElapsedTime();
    cheerleaders.forEach(c => {
        // Jumping up and down
        c.mesh.position.y = c.initialY + Math.abs(Math.sin(time * c.speed + c.phase)) * 0.4;
        // Waving pom poms up and down slightly offsets
        c.pomL.position.y = 0.6 + Math.sin(time * c.speed * 1.5 + c.phase) * 0.25;
        c.pomR.position.y = 0.6 + Math.cos(time * c.speed * 1.5 + c.phase) * 0.25;
        
        // Face the player if they are nearby (use squared distance — no sqrt needed)
        const dist = c.mesh.position.distanceToSquared(player.pos);
        if (dist < 1600) { // 40*40 = 1600
            c.mesh.lookAt(player.pos.x, c.mesh.position.y, player.pos.z);
        }
    });

    // --- Web Line Drawing ---
    if (player.swinging && player.webAnchor) {
        const positions = webLine.geometry.attributes.position.array;
        
        // Start web line from player's head/arms
        positions[0] = player.pos.x;
        positions[1] = player.pos.y + 1.5;
        positions[2] = player.pos.z;
        
        // End web line at anchor
        positions[3] = player.webAnchor.x;
        positions[4] = player.webAnchor.y;
        positions[5] = player.webAnchor.z;
        
        webLine.geometry.attributes.position.needsUpdate = true;
    }

    // --- Third Person Camera Follow ---
    // Smooth camera follow target
    const targetCamX = player.pos.x + cameraDistance * Math.sin(theta) * Math.cos(phi);
    const targetCamY = player.pos.y + cameraDistance * Math.sin(phi);
    const targetCamZ = player.pos.z + cameraDistance * Math.cos(theta) * Math.cos(phi);

    camera.position.x += (targetCamX - camera.position.x) * 0.1;
    camera.position.y += (targetCamY - camera.position.y) * 0.1;
    camera.position.z += (targetCamZ - camera.position.z) * 0.1;
    
    // Look at player position slightly elevated
    camera.lookAt(player.pos.x, player.pos.y + 1.0, player.pos.z);

    renderer.render(scene, camera);
}

// Window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start loop
animate();
