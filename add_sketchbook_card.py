import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

card_markup = """
      <!-- Project Card 4: 3D SKETCHBOOK SHOWCASE -->
      <article class="project-card" style="cursor: pointer;" onclick="openSketchbookModal()">
        <div class="project-preview-box" style="background: linear-gradient(135deg, #1f0b28 0%, #0d0512 100%);">
          <div class="project-preview-overlay">
            <span class="project-kicker">3D INTERACTIVE SHOWCASE</span>
            <div class="project-preview-badge"><i class="fa-solid fa-book-open"></i> GSAP CANVAS</div>
          </div>
          <div class="project-visual-graphic" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 110px; gap: 0.5rem;">
            <i class="fa-solid fa-book-bookmark" style="font-size: 2.5rem; color: #00e5ff;"></i>
            <span style="font-size: 0.8rem; color: #8892b0;">CLICK TO LAUNCH INTERACTIVE SKETCHBOOK</span>
          </div>
        </div>
        <div class="project-details">
          <h3 class="project-title">GSAP 3D Sketchbook</h3>
          <p class="project-desc">Realistic 3D page-flipping book with custom easing curves, depth blur filters, and interactive artwork gallery.</p>
          <div class="project-tags">
            <span class="project-tag">GSAP 3</span>
            <span class="project-tag">CustomEase</span>
            <span class="project-tag">SVG Filters</span>
            <span class="project-tag">3D Transform</span>
          </div>
          <div class="project-links">
            <button class="project-btn primary" onclick="openSketchbookModal(); event.stopPropagation();">// OPEN SKETCHBOOK <i class="fa-solid fa-arrow-up-right-from-square"></i></button>
          </div>
        </div>
      </article>
"""

if 'GSAP 3D Sketchbook' not in html:
    html = html.replace('<!-- Project Card 3 -->', card_markup + '\n      <!-- Project Card 3 -->')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added 3D Sketchbook Showcase Card to index.html")
