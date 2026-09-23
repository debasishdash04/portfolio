import re

# 1. Update styles.css for navbar hover and sketchbook inline section
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Enhance navbar links hover
old_nav_css = r'\.nav-links a \{\s*color: var\(--text-muted\);\s*text-decoration: none;\s*font-weight: 500;\s*transition: color 0\.3s ease;\s*\}\s*\.nav-links a:hover \{\s*color: var\(--accent\);\s*\}'

new_nav_css = """.nav-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  padding-bottom: 4px;
}

.nav-links a:hover {
  color: #00e5ff !important;
  text-shadow: 0 0 12px rgba(0, 229, 255, 0.7);
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: #00e5ff;
  box-shadow: 0 0 8px #00e5ff;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-links a:hover::after {
  width: 100%;
}"""

css = re.sub(old_nav_css, new_nav_css, css)

# Append inline sketchbook section CSS
sketchbook_section_css = """

/* Sketchbook Page Section Styling */
.sketchbook-page-section {
  padding: 6rem 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  z-index: 10;
  position: relative;
}

.sketchbook-inline-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: 100%;
  max-width: 1000px;
  margin: 2rem 0;
}
"""

if '.sketchbook-page-section' not in css:
    css += sketchbook_section_css

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated navbar hover and added section CSS in styles.css")

# 2. Update index.html to insert Sketchbook Section
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

sketchbook_section_html = """
  <!-- 3D Sketchbook Section -->
  <section id="sketchbook" class="sketchbook-page-section">
    <h2 class="section-title">3D SKETCHBOOK SHOWCASE</h2>
    <p style="text-align: center; color: #8892b0; margin-top: -2.5rem; margin-bottom: 2rem; font-size: 1.05rem;">
      Interactive 3D GSAP sketchbook — Click left/right pages or use arrow controls to turn pages
    </p>

    <div class="sketchbook-inline-stage">
      <button class="book-arrow" id="inlinePrevBtn">‹</button>
      <div class="book" id="inlineBookStage">
        <div class="page" id="inlineBookPage"></div>
      </div>
      <button class="book-arrow" id="inlineNextBtn">›</button>
    </div>

    <p class="book-caption" id="inlineBookCaption" style="text-align: center; margin-top: 1rem; color: #00e5ff; font-weight: 600; letter-spacing: 1px; font-size: 1.1rem;"></p>
  </section>
"""

# Change navbar link href back to #sketchbook without alert/preventdefault
html = html.replace('<li><a href="#sketchbook" onclick="openSketchbookModal(); return false;">SKETCHBOOK</a></li>', '<li><a href="#sketchbook">SKETCHBOOK</a></li>')

if 'id="sketchbook"' not in html:
    html = html.replace('<!-- Integrations / Tech Stack Section -->', sketchbook_section_html + '\n  <!-- Integrations / Tech Stack Section -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Inserted Sketchbook Section into index.html")

# 3. Update spline-lazy.js to handle inline sketchbook rendering automatically on DOMContentLoaded
with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

inline_js_logic = """

// --- Inline 3D Sketchbook Logic ---
document.addEventListener("DOMContentLoaded", () => {
  const inlineStage = document.getElementById('inlineBookStage');
  const inlinePage = document.getElementById('inlineBookPage');
  const inlineCaption = document.getElementById('inlineBookCaption');
  const inlinePrevBtn = document.getElementById('inlinePrevBtn');
  const inlineNextBtn = document.getElementById('inlineNextBtn');

  if (!inlineStage || !inlinePage) return;

  let currentInlinePage = 0;
  let inlineFlipTween = null;

  const halfImage = (pageIndex, side) =>
    `<img src="${sketchbookPages[pageIndex].src}" class="${side}">`;

  function showInlinePage(pageIndex) {
    currentInlinePage = pageIndex;
    inlinePage.innerHTML = `
      <div class="half left">${halfImage(pageIndex, "left")}</div>
      <div class="half right">${halfImage(pageIndex, "right")}</div>`;
  }

  function setInlineCaption(title) {
    if (inlineCaption) {
      inlineCaption.textContent = title;
      if (typeof gsap !== 'undefined') {
        gsap.fromTo(inlineCaption, { opacity: 0 }, { opacity: 1, duration: 0.4, overwrite: "auto" });
      }
    }
  }

  function turnInline(direction, duration = 0.85, ease = "pageTurn") {
    if (inlineFlipTween && inlineFlipTween.isActive()) {
      inlineFlipTween.progress(1);
    }

    const goingNext = direction === "next";
    const targetPage = (currentInlinePage + (goingNext ? 1 : -1) + sketchbookPages.length) % sketchbookPages.length;

    const liftSide = goingNext ? "right" : "left";
    const landSide = goingNext ? "left" : "right";

    inlineStage.insertAdjacentHTML("beforeend", `
      <div class="turn">
        <div class="half ${liftSide}">${halfImage(targetPage, liftSide)}</div>
        <div class="flap ${goingNext ? "next" : "prev"}">
          <div class="face">${halfImage(currentInlinePage, liftSide)}</div>
          <div class="face back">${halfImage(targetPage, landSide)}</div>
        </div>
      </div>`);

    setInlineCaption(sketchbookPages[targetPage].title);

    if (typeof gsap !== 'undefined') {
      inlineFlipTween = gsap.to(inlineStage.querySelector(".flap"), {
        rotationY: goingNext ? -180 : 180,
        transformOrigin: goingNext ? "left center" : "right center",
        duration: duration,
        ease: ease,
        onComplete() {
          showInlinePage(targetPage);
          const turnElem = inlineStage.querySelector(".turn");
          if (turnElem) turnElem.remove();
        }
      });
    } else {
      showInlinePage(targetPage);
      const turnElem = inlineStage.querySelector(".turn");
      if (turnElem) turnElem.remove();
    }
  }

  if (inlineNextBtn) inlineNextBtn.onclick = () => turnInline("next");
  if (inlinePrevBtn) inlinePrevBtn.onclick = () => turnInline("prev");

  inlineStage.onclick = event =>
    turnInline(event.offsetX < inlineStage.offsetWidth / 2 ? "prev" : "next");

  showInlinePage(0);
  setInlineCaption(sketchbookPages[0].title);
});
"""

if 'initInlineSketchbook' not in js and 'inlineBookStage' not in js:
    js += inline_js_logic
    with open('spline-lazy.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Appended inline sketchbook JS to spline-lazy.js")
