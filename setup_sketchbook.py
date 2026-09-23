import os
import shutil
import re

# 1. Copy images
src_dir = r"C:\Users\ASUS\Downloads\x-book-main\x-book-main\images"
dest_dir = r"c:\Users\ASUS\New folder\images"

os.makedirs(dest_dir, exist_ok=True)

for filename in os.listdir(src_dir):
    src_file = os.path.join(src_dir, filename)
    dest_file = os.path.join(dest_dir, filename)
    if os.path.isfile(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied {filename} to images/")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add GSAP scripts in head if missing
gsap_scripts = """  <!-- GSAP for Sketchbook Page-Flip -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/CustomEase.min.js"></script>
</head>"""

if 'gsap.min.js' not in html:
    html = html.replace('</head>', gsap_scripts)

# Add SKETCHBOOK link to Navbar
if 'openSketchbookModal' not in html:
    html = html.replace(
        '<li><a href="#projects">PROJECTS</a></li>',
        '<li><a href="#projects">PROJECTS</a></li>\n      <li><a href="#sketchbook" onclick="openSketchbookModal(); return false;">SKETCHBOOK</a></li>'
    )

# Add Sketchbook Modal Markup before </body>
sketchbook_modal_markup = """
  <!-- SVG Filters for Motion Blur -->
  <svg width="0" height="0" aria-hidden="true" style="position:absolute;">
    <filter id="motion-blur-light"><feGaussianBlur stdDeviation="5 0" /></filter>
    <filter id="motion-blur-heavy"><feGaussianBlur stdDeviation="14 0" /></filter>
  </svg>

  <!-- Sketchbook Modal Overlay -->
  <div class="modal-overlay" id="sketchbook-modal">
    <div class="modal-container sketchbook-container">
      <button class="modal-close" onclick="closeModal('sketchbook-modal')">&times;</button>
      
      <div class="modal-header" style="margin-bottom: 2rem;">
        <span class="modal-kicker">INTERACTIVE SHOWCASE</span>
        <h2 class="modal-title">3D Sketchbook</h2>
        <p class="modal-subtitle">Use arrow buttons or click on left/right pages to turn pages</p>
      </div>

      <div class="sketchbook-stage">
        <button class="book-arrow" id="prevBookBtn">‹</button>
        <div class="book" id="bookStage">
          <div class="page" id="bookPage"></div>
        </div>
        <button class="book-arrow" id="nextBookBtn">›</button>
      </div>

      <p class="book-caption" id="bookCaption" style="text-align: center; margin-top: 1.5rem; color: #00e5ff; font-weight: 600; letter-spacing: 1px;"></p>
    </div>
  </div>
"""

if 'id="sketchbook-modal"' not in html:
    html = html.replace('<script src="spline-lazy.js" defer></script>', sketchbook_modal_markup + '\n  <script src="spline-lazy.js" defer></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html for Sketchbook Modal successfully")
