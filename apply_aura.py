import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

aura_markup = """
  <!-- Dot Matrix - Aura Background -->
  <div class="aura-bg" aria-hidden="true">
    <div class="aura-layer-1" aria-hidden="true"></div>
    <div class="aura-layer-2" aria-hidden="true"></div>
    <div class="aura-layer-3" aria-hidden="true"></div>
  </div>
"""

if 'class="aura-bg"' not in html:
    html = html.replace('<body>', '<body>\n' + aura_markup)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added aura markup to index.html")

# 2. Update styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'--bg-color:\s*#[0-9a-fA-F]+;', '--bg-color: #100e0b;', css)

aura_css = """

/* Dot Matrix - Aura Background */
body {
  background-color: #100e0b !important;
}

.aura-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

/* Layer 1 - normal */
.aura-layer-1 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(139,92,246,0.2) 1px, transparent 1px);
  background-size: 20px 20px;
  mix-blend-mode: normal;
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 2 - screen */
.aura-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 40% 40%, rgba(124,58,237,0.6) 0%, transparent 50%);
  mix-blend-mode: screen;
  filter: blur(252px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 3 - screen */
.aura-layer-3 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 70% 65%, rgba(168,85,247,0.4) 0%, transparent 40%);
  mix-blend-mode: screen;
  filter: blur(198px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

@media (max-width: 768px) {
  .aura-layer-2 {
    filter: blur(175px);
  }
  .aura-layer-3 {
    filter: blur(138px);
  }
}
"""

if '.aura-bg' not in css:
    with open('styles.css', 'a', encoding='utf-8') as f:
        f.write(aura_css)
    print("Appended aura CSS to styles.css")
