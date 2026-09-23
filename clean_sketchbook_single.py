import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove sketchbook-modal markup and inline fallback script
html = re.sub(r'<!-- Sketchbook Modal Overlay -->.*?</html>', '</body>\n</html>', html, flags=re.DOTALL)
html = re.sub(r'<!-- Project Card 4: 3D SKETCHBOOK SHOWCASE -->.*?<!-- Project Card 3 -->', '<!-- Project Card 3 -->', html, flags=re.DOTALL)

sketchbook_section_clean = """
  <!-- 3D Sketchbook Section -->
  <section id="sketchbook" class="sketchbook-section">
    <h2 class="section-title">3D SKETCHBOOK SHOWCASE</h2>
    
    <div class="stage">
      <button class="arrow" id="prevButton">‹</button>
      <div class="book" id="bookStage">
        <div class="page" id="bookPage"></div>
      </div>
      <button class="arrow" id="nextButton">›</button>
    </div>

    <p class="caption" id="bookCaption"></p>
  </section>
"""

# Replace existing #sketchbook section
html = re.sub(r'<!-- 3D Sketchbook Section -->.*?<!-- Integrations / Tech Stack Section -->', sketchbook_section_clean + '\n  <!-- Integrations / Tech Stack Section -->', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Cleaned index.html successfully")

# 2. Update styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove old sketchbook CSS and append exact x-book CSS
css = re.sub(r'/\* Sketchbook Modal & 3D Page-Flip Styling \*/.*$', '', css, flags=re.DOTALL)

exact_xbook_css = """
/* 3D Sketchbook Section Styling */
.sketchbook-section {
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  position: relative;
  z-index: 10;
}

.stage {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  width: 100%;
  max-width: 1000px;
}

.caption {
  margin: 1.5rem 0 0 0;
  text-align: center;
  font-size: 14px;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: #00e5ff;
  font-weight: 600;
}

.arrow {
  border: 1px solid rgba(0, 229, 255, 0.3);
  background: rgba(0, 229, 255, 0.08);
  font-size: 32px;
  color: #00e5ff;
  cursor: pointer;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.arrow:hover {
  background: #00e5ff;
  color: #050505;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
  transform: scale(1.1);
}

.book {
  position: relative;
  width: min(720px, 78vw);
  aspect-ratio: 16 / 9;
  perspective: 2600px;
  cursor: pointer;
}

.book::before {
  content: "";
  position: absolute;
  inset: 9% 19% 3% 21%;
  border-radius: 18px;
  background: rgba(0, 229, 255, 0.15);
  filter: blur(28px);
}

.book * {
  pointer-events: none;
}

.page,
.turn {
  display: contents;
}

.half,
.face {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  overflow: hidden;
}

.half {
  width: 50%;
}

.half.right {
  left: 50%;
}

.half img,
.face img {
  display: block;
  width: 200%;
  height: 100%;
  object-fit: cover;
  user-select: none;
}

img.right {
  margin-left: -100%;
}

.flap {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 50%;
  transform-style: preserve-3d;
  will-change: transform;
}

.flap.next {
  left: 50%;
}

.face {
  width: 100%;
  backface-visibility: hidden;
}

.face.back {
  transform: rotateY(180deg);
}

.book.blur-light img {
  filter: url(#motion-blur-light);
}

.book.blur-heavy img {
  filter: url(#motion-blur-heavy);
}
"""

css += exact_xbook_css

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated styles.css successfully")

# 3. Update spline-lazy.js
with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove old sketchbook JS and append exact x-book JS
js = re.sub(r'// --- 3D Sketchbook Modal Logic ---.*$', '', js, flags=re.DOTALL)

exact_xbook_js = """
// --- 3D Sketchbook Logic ---
document.addEventListener("DOMContentLoaded", () => {
  const pages = [
    { src: "images/kyoto-performing-arts.png", title: "Kyoto Performing Arts Hall" },
    { src: "images/kyoto.png", title: "Kyoto Garden Museum" },
    { src: "images/castle.png", title: "Western Castle" },
    { src: "images/taipei-market.png", title: "Taipei Night Market" },
    { src: "images/osaka.png", title: "Osaka Castle" },
    { src: "images/tokyo-museum.png", title: "Tokyo National Museum" }
  ];

  const bookStage = document.getElementById("bookStage");
  const bookPage = document.getElementById("bookPage");
  const bookCaption = document.getElementById("bookCaption");
  const prevButton = document.getElementById("prevButton");
  const nextButton = document.getElementById("nextButton");

  if (!bookStage || !bookPage) return;

  if (typeof gsap !== 'undefined' && typeof CustomEase !== 'undefined') {
    try {
      gsap.registerPlugin(CustomEase);
      CustomEase.create("pageTurn", ".42,.05,.25,1");
    } catch(e) {}
  }

  let currentPage = 0;
  let flipTween = null;
  let introPlaying = false;

  const halfImage = (pageIndex, side) =>
    `<img src="${pages[pageIndex].src}" class="${side}">`;

  function showPage(pageIndex) {
    currentPage = pageIndex;
    bookPage.innerHTML = `
      <div class="half left">${halfImage(pageIndex, "left")}</div>
      <div class="half right">${halfImage(pageIndex, "right")}</div>`;
  }

  function setCaption(title) {
    if (bookCaption) {
      bookCaption.textContent = title;
      if (typeof gsap !== 'undefined') {
        gsap.fromTo(bookCaption, { opacity: 0 }, { opacity: 1, duration: 0.4, overwrite: "auto" });
      }
    }
  }

  function turn(direction, duration = 0.85, ease = "pageTurn", onDone) {
    if (flipTween && flipTween.isActive()) {
      flipTween.progress(1);
    }

    const goingNext = direction === "next";
    const targetPage = (currentPage + (goingNext ? 1 : -1) + pages.length) % pages.length;

    const liftSide = goingNext ? "right" : "left";
    const landSide = goingNext ? "left" : "right";

    bookStage.insertAdjacentHTML("beforeend", `
      <div class="turn">
        <div class="half ${liftSide}">${halfImage(targetPage, liftSide)}</div>
        <div class="flap ${goingNext ? "next" : "prev"}">
          <div class="face">${halfImage(currentPage, liftSide)}</div>
          <div class="face back">${halfImage(targetPage, landSide)}</div>
        </div>
      </div>`);

    setCaption(pages[targetPage].title);

    if (typeof gsap !== 'undefined') {
      flipTween = gsap.to(bookStage.querySelector(".flap"), {
        rotationY: goingNext ? -180 : 180,
        transformOrigin: goingNext ? "left center" : "right center",
        duration: duration,
        ease: ease,
        onComplete() {
          showPage(targetPage);
          const turnElem = bookStage.querySelector(".turn");
          if (turnElem) turnElem.remove();
          if (onDone) onDone();
        }
      });
    } else {
      showPage(targetPage);
      const turnElem = bookStage.querySelector(".turn");
      if (turnElem) turnElem.remove();
      if (onDone) onDone();
    }
  }

  function riffle(step = 0) {
    if (!introPlaying || step >= pages.length) {
      introPlaying = false;
      bookStage.classList.remove("blur-light", "blur-heavy");
      return;
    }

    const bell = Math.sin(Math.PI * step / (pages.length - 1));
    bookStage.classList.toggle("blur-light", bell > 0.25 && bell <= 0.6);
    bookStage.classList.toggle("blur-heavy", bell > 0.6);

    turn("next", 0.2 - 0.15 * bell, "none", () => riffle(step + 1));
  }

  function navigate(direction) {
    introPlaying = false;
    turn(direction);
  }

  if (nextButton) nextButton.onclick = () => navigate("next");
  if (prevButton) prevButton.onclick = () => navigate("prev");

  bookStage.onclick = event =>
    navigate(event.offsetX < bookStage.offsetWidth / 2 ? "prev" : "next");

  showPage(0);
  setCaption(pages[0].title);

  // Auto-play intro riffle when section enters viewport
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !introPlaying && currentPage === 0) {
        if (typeof gsap !== 'undefined') {
          gsap.delayedCall(0.2, () => {
            introPlaying = true;
            riffle();
          });
        }
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  observer.observe(bookStage);
});
"""

js += exact_xbook_js

with open('spline-lazy.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated spline-lazy.js successfully")
