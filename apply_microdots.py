import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace aura CSS with exact Microdots specification
old_aura_pattern = r'/\* Dot Matrix - Aura Background \*/.*?(?=$|\n/\* [A-Z])'

microdots_css = """/* Microdots - Aura Background */
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
  background: radial-gradient(circle, rgba(147,197,253,0.3) 1px, transparent 1.5px);
  background-size: 14px 14px;
  mix-blend-mode: normal;
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 2 - screen */
.aura-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 65% 50% at 50% 45%, rgba(59,130,246,0.35) 0%, transparent 75%);
  mix-blend-mode: screen;
  filter: blur(234px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 3 - screen */
.aura-layer-3 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 25%, rgba(125,211,252,0.3) 0%, transparent 30%);
  mix-blend-mode: screen;
  filter: blur(162px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

@media (max-width: 768px) {
  .aura-layer-2 {
    filter: blur(163px);
  }
  .aura-layer-3 {
    filter: blur(113px);
  }
}
"""

css = re.sub(old_aura_pattern, microdots_css, css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied Microdots Aura Background successfully to styles.css")
