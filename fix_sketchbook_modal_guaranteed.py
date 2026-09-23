import re

# 1. Update spline-lazy.js to make initSketchbook and startSketchbookRiffle clean globals
sketchbook_js_clean = """

// --- 3D Sketchbook Modal Logic ---
const sketchbookPages = [
  { src: "images/kyoto-performing-arts.png", title: "Kyoto Performing Arts Hall" },
  { src: "images/kyoto.png", title: "Kyoto Garden Museum" },
  { src: "images/castle.png", title: "Western Castle" },
  { src: "images/taipei-market.png", title: "Taipei Night Market" },
  { src: "images/osaka.png", title: "Osaka Castle" },
  { src: "images/tokyo-museum.png", title: "Tokyo National Museum" }
];

let currentBookPage = 0;
let bookFlipTween = null;
let bookIntroPlaying = false;
let sketchbookInitialized = false;

window.initSketchbook = function() {
  const bookStage = document.getElementById('bookStage');
  const bookPage = document.getElementById('bookPage');
  const bookCaption = document.getElementById('bookCaption');
  const prevBookBtn = document.getElementById('prevBookBtn');
  const nextBookBtn = document.getElementById('nextBookBtn');

  if (!bookStage || !bookPage) return;
  if (sketchbookInitialized) {
    showBookPage(currentBookPage);
    return;
  }
  sketchbookInitialized = true;

  if (typeof gsap !== 'undefined' && typeof CustomEase !== 'undefined') {
    try {
      gsap.registerPlugin(CustomEase);
      CustomEase.create("pageTurn", ".42,.05,.25,1");
    } catch(e) {}
  }

  const halfImage = (pageIndex, side) =>
    `<img src="${sketchbookPages[pageIndex].src}" class="${side}">`;

  function showBookPage(pageIndex) {
    currentBookPage = pageIndex;
    bookPage.innerHTML = `
      <div class="half left">${halfImage(pageIndex, "left")}</div>
      <div class="half right">${halfImage(pageIndex, "right")}</div>`;
  }
  window.showBookPage = showBookPage;

  function setBookCaption(title) {
    if (bookCaption) {
      bookCaption.textContent = title;
      if (typeof gsap !== 'undefined') {
        gsap.fromTo(bookCaption, { opacity: 0 }, { opacity: 1, duration: 0.4, overwrite: "auto" });
      }
    }
  }

  function turnBook(direction, duration = 0.85, ease = "pageTurn", onDone) {
    if (bookFlipTween && bookFlipTween.isActive()) {
      bookFlipTween.progress(1);
    }

    const goingNext = direction === "next";
    const targetPage = (currentBookPage + (goingNext ? 1 : -1) + sketchbookPages.length) % sketchbookPages.length;

    const liftSide = goingNext ? "right" : "left";
    const landSide = goingNext ? "left" : "right";

    bookStage.insertAdjacentHTML("beforeend", `
      <div class="turn">
        <div class="half ${liftSide}">${halfImage(targetPage, liftSide)}</div>
        <div class="flap ${goingNext ? "next" : "prev"}">
          <div class="face">${halfImage(currentBookPage, liftSide)}</div>
          <div class="face back">${halfImage(targetPage, landSide)}</div>
        </div>
      </div>`);

    setBookCaption(sketchbookPages[targetPage].title);

    if (typeof gsap !== 'undefined') {
      bookFlipTween = gsap.to(bookStage.querySelector(".flap"), {
        rotationY: goingNext ? -180 : 180,
        transformOrigin: goingNext ? "left center" : "right center",
        duration: duration,
        ease: ease,
        onComplete() {
          showBookPage(targetPage);
          const turnElem = bookStage.querySelector(".turn");
          if (turnElem) turnElem.remove();
          if (onDone) onDone();
        }
      });
    } else {
      showBookPage(targetPage);
      const turnElem = bookStage.querySelector(".turn");
      if (turnElem) turnElem.remove();
      if (onDone) onDone();
    }
  }
  window.turnBook = turnBook;

  function riffleBook(step = 0) {
    if (!bookIntroPlaying || step >= sketchbookPages.length) {
      bookIntroPlaying = false;
      bookStage.classList.remove("blur-light", "blur-heavy");
      return;
    }

    const bell = Math.sin(Math.PI * step / (sketchbookPages.length - 1));
    bookStage.classList.toggle("blur-light", bell > 0.25 && bell <= 0.6);
    bookStage.classList.toggle("blur-heavy", bell > 0.6);

    turnBook("next", 0.25 - 0.15 * bell, "none", () => riffleBook(step + 1));
  }

  function navigateBook(direction) {
    bookIntroPlaying = false;
    turnBook(direction);
  }

  if (nextBookBtn) nextBookBtn.onclick = () => navigateBook("next");
  if (prevBookBtn) prevBookBtn.onclick = () => navigateBook("prev");

  bookStage.onclick = event =>
    navigateBook(event.offsetX < bookStage.offsetWidth / 2 ? "prev" : "next");

  showBookPage(0);
  setBookCaption(sketchbookPages[0].title);

  window.startSketchbookRiffle = function() {
    if (typeof gsap !== 'undefined') {
      gsap.delayedCall(0.3, () => {
        bookIntroPlaying = true;
        riffleBook();
      });
    }
  };
};

window.openSketchbookModal = function() {
  const modal = document.getElementById('sketchbook-modal');
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  if (window.initSketchbook) {
    window.initSketchbook();
  }
  if (window.startSketchbookRiffle) {
    window.startSketchbookRiffle();
  }
};
"""

with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the sketchbook block in spline-lazy.js
js_pattern = r'// --- 3D Sketchbook Modal Logic ---.*$'
js = re.sub(js_pattern, sketchbook_js_clean.strip(), js, flags=re.DOTALL)

with open('spline-lazy.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated spline-lazy.js with clean global sketchbook functions")

# 2. Update index.html to add global click inline script & Project Showcase Card
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

inline_script = """
  <script>
    function openSketchbookModal() {
      const modal = document.getElementById('sketchbook-modal');
      if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
      if (typeof window.initSketchbook === 'function') {
        window.initSketchbook();
      }
      if (typeof window.startSketchbookRiffle === 'function') {
        window.startSketchbookRiffle();
      }
    }
  </script>
"""

if 'function openSketchbookModal()' not in html:
    html = html.replace('</body>', inline_script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added inline script fallback to index.html")
