import re

# 1. Clean index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove GSAP scripts
html = re.sub(r'\s*<!-- GSAP for Sketchbook Page-Flip -->\s*<script src="https://cdn\.jsdelivr\.net/npm/gsap@3/dist/gsap\.min\.js"></script>\s*<script src="https://cdn\.jsdelivr\.net/npm/gsap@3/dist/CustomEase\.min\.js"></script>', '', html)

# Remove SKETCHBOOK link from navbar
html = re.sub(r'\s*<li><a href="#sketchbook">SKETCHBOOK</a></li>', '', html)

# Remove Sketchbook Section
html = re.sub(r'\s*<!-- 3D Sketchbook Section -->\s*<section id="sketchbook".*?</section>', '', html, flags=re.DOTALL)

# Remove SVG filters for motion blur and make sure spline-lazy.js is linked before </body>
html = re.sub(r'\s*<!-- SVG Filters for Motion Blur -->\s*<svg width="0" height="0" aria-hidden="true" style="position:absolute;">.*?</svg>', '', html, flags=re.DOTALL)

# Clean up any duplicate or misplaced closing tags before </body>
if '<script src="spline-lazy.js" defer></script>' not in html:
    html = re.sub(r'\s*</body>', '\n  <script src="spline-lazy.js" defer></script>\n</body>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cleaned index.html")

# 2. Clean styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\s*/\* (?:3D )?Sketchbook.*$', '', css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Cleaned styles.css")

# 3. Clean spline-lazy.js
with open('spline-lazy.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r'\s*// --- 3D Sketchbook Logic.*$', '', js, flags=re.DOTALL)

with open('spline-lazy.js', 'w', encoding='utf-8') as f:
    f.write(js.strip() + '\n')
print("Cleaned spline-lazy.js")
