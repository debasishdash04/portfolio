import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Fix body bg-color var to match #100e0b
css = css.replace('--bg-color: #050505;', '--bg-color: #100e0b;')
css = css.replace('background-color: var(--bg-color);', 'background-color: #100e0b;')

# 2. Replace the entire Microdots block with exact spec values + correct section handling
old_block = re.search(r'/\* Microdots - Aura Background \*/.*?(?=\n/\*|\Z)', css, re.DOTALL)
if old_block:
    css = css[:old_block.start()] + css[old_block.end():]

new_aura = """/* Microdots - Aura */
/* Base color on body — blend modes composite against this */
.aura-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
  /* NO background-color here — layers blend against body #100e0b */
}

/* Layer 1 - normal, fine dot lattice */
.aura-layer-1 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(147,197,253,0.16) 1px, transparent 1.5px);
  background-size: 14px 14px;
  mix-blend-mode: normal;
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 2 - screen, central blue ellipse glow */
.aura-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 65% 50% at 50% 45%, rgba(59,130,246,0.26) 0%, transparent 75%);
  mix-blend-mode: screen;
  filter: blur(234px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

/* Layer 3 - screen, top-right sky blue accent */
.aura-layer-3 {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 25%, rgba(125,211,252,0.22) 0%, transparent 30%);
  mix-blend-mode: screen;
  filter: blur(162px);
  transform: translateZ(0);
  will-change: transform;
  pointer-events: none;
}

@media (max-width: 768px) {
  .aura-layer-2 { filter: blur(163px); }
  .aura-layer-3 { filter: blur(113px); }
}

/* All sections sit above the fixed aura layer */
.hero,
.services-section,
.projects-section,
.integrations-section,
.blog-section,
.contact-section,
footer {
  position: relative;
  z-index: 2;
}

/* Cards must be semi-transparent so dots show through */
.service-card {
  background: rgba(10, 10, 18, 0.72) !important;
  backdrop-filter: blur(12px) !important;
}

.project-card {
  background: rgba(10, 10, 18, 0.72) !important;
  backdrop-filter: blur(12px) !important;
}

.blog-card {
  background: rgba(10, 10, 18, 0.72) !important;
  backdrop-filter: blur(12px) !important;
}

.logo-panel {
  background: rgba(10, 10, 18, 0.55) !important;
  backdrop-filter: blur(8px) !important;
}

.contact-box {
  background: rgba(10, 10, 18, 0.72) !important;
  backdrop-filter: blur(12px) !important;
}

"""

css = css.rstrip() + '\n\n' + new_aura

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied exact Microdots Aura spec to styles.css")
