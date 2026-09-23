import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace aura CSS with vibrant, high-visibility dot lattice & glow parameters
old_aura_pattern = r'/\* Dot Matrix - Aura Background \*/.*?(?=$|\n/\* [A-Z])'

new_aura_css = """/* Dot Matrix - Aura Background */
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

/* Layer 1 - Dot Lattice */
.aura-layer-1 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.45) 1.5px, transparent 1.5px);
  background-size: 24px 24px;
  mix-blend-mode: normal;
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
  opacity: 0.85;
}

/* Layer 2 - Screen Glow 1 */
.aura-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 35% 35%, rgba(147, 51, 234, 0.75) 0%, transparent 60%);
  mix-blend-mode: screen;
  filter: blur(140px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 3 - Screen Glow 2 */
.aura-layer-3 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 75% 65%, rgba(192, 132, 252, 0.55) 0%, transparent 55%);
  mix-blend-mode: screen;
  filter: blur(120px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Translucent Card & Section Fills so Aura Lattice shines through */
.service-card {
  background: rgba(15, 15, 20, 0.75) !important;
  backdrop-filter: blur(8px);
}

.project-card {
  background: rgba(15, 15, 20, 0.75) !important;
  backdrop-filter: blur(8px);
}

.blog-card {
  background: rgba(15, 15, 20, 0.75) !important;
  backdrop-filter: blur(8px);
}

.logo-panel {
  background: rgba(15, 15, 20, 0.6) !important;
  backdrop-filter: blur(8px);
}

@media (max-width: 768px) {
  .aura-layer-2 {
    filter: blur(100px);
  }
  .aura-layer-3 {
    filter: blur(90px);
  }
}
"""

css = re.sub(old_aura_pattern, new_aura_css, css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated aura visibility in styles.css")
