/**
 * Interactive Breakout Game ("HELLO WORLD")
 * Recreates the dot-matrix brick breaker widget with proper spacing,
 * smooth controllable ball speed, and 3-chance lives system.
 */

(function() {
  const canvas = document.getElementById('breakout-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const container = canvas.parentElement;

  // Font Map: 5x7 grid per character with clean rounded matrix typography
  const FONT_5x7 = {
    'H': [
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,1,1,1,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1]
    ],
    'E': [
      [1,1,1,1,1],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,1,1,1,0],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,1,1,1,1]
    ],
    'L': [
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,0,0,0,0],
      [1,1,1,1,1]
    ],
    'O': [
      [0,1,1,1,0],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [0,1,1,1,0]
    ],
    'W': [
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,1,0,1],
      [1,0,1,0,1],
      [1,1,0,1,1],
      [1,0,0,0,1]
    ],
    'R': [
      [1,1,1,1,0],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,1,1,1,0],
      [1,0,1,0,0],
      [1,0,0,1,0],
      [1,0,0,0,1]
    ],
    'D': [
      [1,1,1,1,0],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,0,0,0,1],
      [1,1,1,1,0]
    ]
  };

  const MAX_LIVES = 3;
  let lives = MAX_LIVES;

  let width = 0;
  let height = 0;
  let dpr = window.devicePixelRatio || 1;

  let bricks = [];
  let particles = [];
  let ball = { x: 0, y: 0, vx: 0, vy: 0, radius: 7, isHolding: false, holdTimer: 0, speed: 3.5 };
  let paddle = { x: 0, y: 0, width: 140, height: 12, targetX: 0 };
  let isAutoPlay = true;
  let lastUserActivity = 0;
  let isMouseOver = false;
  let animationFrameId = null;

  function updateLivesUI() {
    const dotsContainer = document.getElementById('game-lives-indicator');
    if (!dotsContainer) return;

    const dots = dotsContainer.querySelectorAll('span');
    dots.forEach((dot, index) => {
      if (index < lives) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }

  function initBricks() {
    bricks = [];
    const line1 = "HELLO";
    const line2 = "WORLD";

    const charWidth = 5;
    const charHeight = 7;
    // Responsive spacing between characters and lines based on canvas width
    const charSpacing = width < 420 ? 1 : (width < 640 ? 2 : 3);
    const lineSpacing = width < 420 ? 2 : (width < 640 ? 3 : 4);

    const totalColsLine1 = line1.length * charWidth + (line1.length - 1) * charSpacing;
    const totalColsLine2 = line2.length * charWidth + (line2.length - 1) * charSpacing;
    const maxCols = Math.max(totalColsLine1, totalColsLine2);
    const totalRows = charHeight * 2 + lineSpacing;

    // Calculate dynamic brick size with safety margins so words fit perfectly inside canvas
    const availableWidth = width * 0.86;
    const maxBlockByWidth = Math.floor(availableWidth / maxCols);
    const maxBlockByHeight = Math.floor((height * 0.50) / totalRows);
    let blockSize = Math.min(maxBlockByWidth, maxBlockByHeight);
    blockSize = Math.max(4, Math.min(blockSize, 22));

    const brickMargin = Math.max(1, Math.floor(blockSize * 0.18));
    const renderBlockSize = Math.max(3, blockSize - brickMargin);

    const totalWidth = maxCols * blockSize;
    const startX = Math.floor((width - totalWidth) / 2);
    const startY = Math.floor(height * 0.06); // Clean top offset

    // Helper to generate bricks for a word
    function layoutWord(word, rowOffsetBlocks) {
      const wordCols = word.length * charWidth + (word.length - 1) * charSpacing;
      const wordStartX = startX + Math.floor((totalWidth - wordCols * blockSize) / 2);

      for (let i = 0; i < word.length; i++) {
        const char = word[i];
        const matrix = FONT_5x7[char];
        if (!matrix) continue;

        const charX = wordStartX + i * (charWidth + charSpacing) * blockSize;
        const charY = startY + rowOffsetBlocks * blockSize;

        for (let r = 0; r < charHeight; r++) {
          for (let c = 0; c < charWidth; c++) {
            if (matrix[r][c] === 1) {
              bricks.push({
                x: charX + c * blockSize,
                y: charY + r * blockSize,
                w: renderBlockSize,
                h: renderBlockSize,
                alive: true
              });
            }
          }
        }
      }
    }

    layoutWord(line1, 0);
    layoutWord(line2, charHeight + lineSpacing);
  }

  function resetBall(delayLaunch = true) {
    ball.radius = Math.max(5, Math.min(7.5, width * 0.0075));
    ball.x = paddle.x + paddle.width / 2;
    ball.y = paddle.y - ball.radius - 4;
    
    // Smooth, relaxed, controllable arcade speed
    ball.speed = Math.max(2.8, Math.min(4.0, width * 0.0036));
    const angle = (Math.random() * 0.5 - 0.25) - Math.PI / 2; // upwards with slight randomized tilt
    ball.vx = Math.sin(angle) * ball.speed;
    ball.vy = -Math.abs(Math.cos(angle) * ball.speed);

    if (delayLaunch) {
      ball.isHolding = true;
      ball.holdTimer = 30; // Brief ~0.5s pause before launch
    } else {
      ball.isHolding = false;
      ball.holdTimer = 0;
    }
  }

  function resize() {
    const rect = container.getBoundingClientRect();
    width = rect.width;
    // Generous canvas height so letters and paddle have plenty of separation
    height = Math.max(500, Math.min(620, Math.floor(window.innerHeight * 0.72)));

    dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';

    ctx.resetTransform?.();
    ctx.scale(dpr, dpr);

    paddle.width = Math.max(55, Math.min(160, width * 0.20));
    paddle.height = Math.max(10, Math.min(14, height * 0.024));
    paddle.y = height - paddle.height - 24; // Paddle anchored cleanly at the very bottom
    paddle.x = (width - paddle.width) / 2;
    paddle.targetX = paddle.x;

    initBricks();
    resetBall(false);
    updateLivesUI();
  }

  // Handle Mouse & Touch Input
  function handleMove(clientX) {
    const rect = canvas.getBoundingClientRect();
    const relativeX = clientX - rect.left;
    paddle.targetX = relativeX - paddle.width / 2;
    isAutoPlay = false;
    lastUserActivity = Date.now();
  }

  canvas.addEventListener('mousemove', (e) => {
    isMouseOver = true;
    handleMove(e.clientX);
  });

  canvas.addEventListener('mouseenter', () => {
    isMouseOver = true;
    isAutoPlay = false;
    lastUserActivity = Date.now();
  });

  canvas.addEventListener('mouseleave', () => {
    isMouseOver = false;
  });

  canvas.addEventListener('touchmove', (e) => {
    if (e.touches.length > 0) {
      handleMove(e.touches[0].clientX);
    }
  }, { passive: true });

  function spawnParticles(x, y, color) {
    const count = 6;
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 2.5 + 1;
      particles.push({
        x: x,
        y: y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: Math.random() * 2.5 + 1.5,
        life: 1,
        color: color || '#ffffff'
      });
    }
  }

  function handleBallLoss() {
    lives--;
    updateLivesUI();

    if (lives > 0) {
      // Still have chances left -> respawn ball
      resetBall(true);
    } else {
      // All 3 chances lost -> Rebuild everything from start!
      lives = MAX_LIVES;
      updateLivesUI();
      initBricks();
      resetBall(true);
    }
  }

  function update() {
    // Auto-pilot if inactive for 2 seconds
    if (!isMouseOver && Date.now() - lastUserActivity > 2000) {
      isAutoPlay = true;
    }

    if (isAutoPlay) {
      // Predict ball position smoothly
      const target = ball.x - paddle.width / 2 + (ball.vx * 3);
      paddle.targetX += (target - paddle.targetX) * 0.12;
    }

    // Smooth paddle movement
    paddle.targetX = Math.max(0, Math.min(width - paddle.width, paddle.targetX));
    paddle.x += (paddle.targetX - paddle.x) * 0.25;

    // Holding launch state
    if (ball.isHolding) {
      ball.x = paddle.x + paddle.width / 2;
      ball.y = paddle.y - ball.radius - 4;
      ball.holdTimer--;
      if (ball.holdTimer <= 0) {
        ball.isHolding = false;
      }
      return;
    }

    // Ball movement
    ball.x += ball.vx;
    ball.y += ball.vy;

    // Wall collisions
    if (ball.x - ball.radius <= 0) {
      ball.x = ball.radius;
      ball.vx = Math.abs(ball.vx);
    } else if (ball.x + ball.radius >= width) {
      ball.x = width - ball.radius;
      ball.vx = -Math.abs(ball.vx);
    }

    if (ball.y - ball.radius <= 0) {
      ball.y = ball.radius;
      ball.vy = Math.abs(ball.vy);
    }

    // Paddle collision
    if (
      ball.y + ball.radius >= paddle.y &&
      ball.y - ball.radius <= paddle.y + paddle.height &&
      ball.x >= paddle.x - ball.radius &&
      ball.x <= paddle.x + paddle.width + ball.radius &&
      ball.vy > 0
    ) {
      ball.y = paddle.y - ball.radius;
      
      // Calculate bounce angle based on strike point on paddle
      const hitPoint = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
      const maxBounceAngle = Math.PI / 3; // 60 deg
      const bounceAngle = hitPoint * maxBounceAngle;
      
      ball.vx = ball.speed * Math.sin(bounceAngle);
      ball.vy = -ball.speed * Math.cos(bounceAngle);

      spawnParticles(ball.x, paddle.y, '#ffffff');
    }

    // Bottom loss -> Handle 3-chance logic
    if (ball.y - ball.radius > height) {
      handleBallLoss();
      return;
    }

    // Brick collisions
    let aliveCount = 0;
    for (let i = 0; i < bricks.length; i++) {
      const b = bricks[i];
      if (!b.alive) continue;
      aliveCount++;

      // Check collision between ball and brick rect
      const closestX = Math.max(b.x, Math.min(ball.x, b.x + b.w));
      const closestY = Math.max(b.y, Math.min(ball.y, b.y + b.h));
      const distanceX = ball.x - closestX;
      const distanceY = ball.y - closestY;
      const distanceSquared = distanceX * distanceX + distanceY * distanceY;

      if (distanceSquared < ball.radius * ball.radius) {
        b.alive = false;
        spawnParticles(b.x + b.w / 2, b.y + b.h / 2, '#ffffff');

        // Determine reflection axis
        const prevBallX = ball.x - ball.vx;
        const prevBallY = ball.y - ball.vy;

        if (prevBallX < b.x || prevBallX > b.x + b.w) {
          ball.vx = -ball.vx;
        }
        if (prevBallY < b.y || prevBallY > b.y + b.h) {
          ball.vy = -ball.vy;
        }
        break; // 1 collision per frame
      }
    }

    // Rebuild all bricks if fully cleared
    if (aliveCount === 0) {
      lives = MAX_LIVES;
      updateLivesUI();
      initBricks();
      resetBall(true);
    }

    // Update particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= 0.035;
      if (p.life <= 0) {
        particles.splice(i, 1);
      }
    }
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    // 1. Draw Ghost / Broken Bricks first (faint dark silhouette)
    for (let i = 0; i < bricks.length; i++) {
      const b = bricks[i];
      if (!b.alive) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.07)';
        const radius = Math.min(2, b.w / 4);
        ctx.beginPath();
        ctx.roundRect(b.x, b.y, b.w, b.h, radius);
        ctx.fill();
      }
    }

    // 2. Draw Active / Solid White Bricks
    for (let i = 0; i < bricks.length; i++) {
      const b = bricks[i];
      if (b.alive) {
        ctx.fillStyle = '#ffffff';
        const radius = Math.min(2, b.w / 4);
        ctx.beginPath();
        ctx.roundRect(b.x, b.y, b.w, b.h, radius);
        ctx.fill();
      }
    }

    // 3. Draw Particles
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      ctx.fillStyle = `rgba(255, 255, 255, ${Math.max(0, p.life)})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }

    // 4. Draw Ball
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();

    // 5. Draw Paddle (Sleek rounded pill)
    ctx.fillStyle = '#e4e4e7';
    ctx.beginPath();
    ctx.roundRect(paddle.x, paddle.y, paddle.width, paddle.height, paddle.height / 2);
    ctx.fill();
  }

  function loop() {
    update();
    draw();
    animationFrameId = requestAnimationFrame(loop);
  }

  // Initialize
  window.addEventListener('resize', resize);
  
  // Use IntersectionObserver to pause game when out of viewport to save CPU
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (!animationFrameId) {
          loop();
        }
      } else {
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
          animationFrameId = null;
        }
      }
    });
  }, { threshold: 0.1 });

  observer.observe(container);

  // Initial layout
  setTimeout(resize, 50);
})();
