import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_aura_pattern = r'/\* Microdots - Aura Background \*/.*?(?=$|\n/\* [A-Z])'

boosted_microdots_css = """/* Microdots - Aura Background */
body {
  background-color: #100e0b !important;
}

.aura-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1; /* Render above body base color, below section content */
}

/* Layer 1 - Microdot Grid */
.aura-layer-1 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(147, 197, 253, 0.65) 1.5px, transparent 1.5px);
  background-size: 22px 22px;
  mix-blend-mode: normal;
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
  opacity: 0.9;
}

/* Layer 2 - Blue Core Glow */
.aura-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 65% 50% at 50% 45%, rgba(59, 130, 246, 0.45) 0%, transparent 75%);
  mix-blend-mode: screen;
  filter: blur(120px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 3 - Sky Blue Glow */
.aura-layer-3 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 25%, rgba(125, 211, 252, 0.4) 0%, transparent 35%);
  mix-blend-mode: screen;
  filter: blur(100px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Ensure all page sections sit above aura layers with z-index */
.hero,
.services-section,
.projects-section,
.integrations-section,
.industries-section,
.dashboard-section,
.cta-section,
.footer {
  position: relative;
  z-index: 2;
  background: transparent !important;
}

@media (max-width: 768px) {
  .aura-layer-2 {
    filter: blur(80px);
  }
  .aura-layer-3 {
    filter: blur(70px);
  }
}
"""

css = re.sub(old_aura_pattern, boosted_microdots_css, css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated hero & global microdots visibility in styles.css")
