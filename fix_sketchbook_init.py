import re

with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace initSketchbook logic to prevent early lock out
old_init = """function initSketchbook() {
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

  if (!bookStage || !bookPage) return;"""

new_init = """function initSketchbook() {
  const bookStage = document.getElementById('bookStage');
  const bookPage = document.getElementById('bookPage');
  const bookCaption = document.getElementById('bookCaption');
  const prevBookBtn = document.getElementById('prevBookBtn');
  const nextBookBtn = document.getElementById('nextBookBtn');

  if (!bookStage || !bookPage) return;
  if (sketchbookInitialized) return;
  sketchbookInitialized = true;

  if (typeof gsap !== 'undefined' && typeof CustomEase !== 'undefined') {
    try {
      gsap.registerPlugin(CustomEase);
      CustomEase.create("pageTurn", ".42,.05,.25,1");
    } catch(e) {}
  }"""

if 'if (!bookStage || !bookPage) return;\n  if (sketchbookInitialized) return;' not in js:
    js = js.replace(old_init, new_init)
    with open('spline-lazy.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed initSketchbook early lockout bug")
