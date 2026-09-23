import re

sketchbook_css = """

/* Sketchbook Modal & 3D Page-Flip Styling */
.sketchbook-container {
  max-width: 900px !important;
  background: rgba(13, 19, 33, 0.96) !important;
  border: 1px solid rgba(0, 229, 255, 0.3) !important;
  box-shadow: 0 0 50px rgba(0, 229, 255, 0.2) !important;
}

.sketchbook-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  width: 100%;
  margin: 1rem 0;
}

.book-arrow {
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

.book-arrow:hover {
  background: #00e5ff;
  color: #050505;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
  transform: scale(1.1);
}

.book {
  position: relative;
  width: min(720px, 75vw);
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

.page, .turn {
  display: contents;
}

.half, .face {
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

.half img, .face img {
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

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.sketchbook-container' not in css:
    with open('styles.css', 'a', encoding='utf-8') as f:
        f.write(sketchbook_css)
    print("Appended Sketchbook CSS")

sketchbook_js = """

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

function initSketchbook() {
  if (sketchbookInitialized) return;
  sketchbookInitialized = true;

  if (typeof gsap !== 'undefined' && typeof CustomEase !== 'undefined') {
    gsap.registerPlugin(CustomEase);
    try { CustomEase.create("pageTurn", ".42,.05,.25,1"); } catch(e) {}
  }

  const bookStage = document.getElementById('bookStage');
  const bookPage = document.getElementById('bookPage');
  const bookCaption = document.getElementById('bookCaption');
  const prevBookBtn = document.getElementById('prevBookBtn');
  const nextBookBtn = document.getElementById('nextBookBtn');

  if (!bookStage || !bookPage) return;

  const halfImage = (pageIndex, side) =>
    `<img src="${sketchbookPages[pageIndex].src}" class="${side}">`;

  function showBookPage(pageIndex) {
    currentBookPage = pageIndex;
    bookPage.innerHTML = `
      <div class="half left">${halfImage(pageIndex, "left")}</div>
      <div class="half right">${halfImage(pageIndex, "right")}</div>`;
  }

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
}

window.openSketchbookModal = function() {
  initSketchbook();
  openModal('sketchbook-modal');
  if (window.startSketchbookRiffle) {
    window.startSketchbookRiffle();
  }
};
"""

with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

if 'openSketchbookModal' not in js:
    with open('spline-lazy.js', 'a', encoding='utf-8') as f:
        f.write(sketchbook_js)
    print("Appended Sketchbook JS to spline-lazy.js")
