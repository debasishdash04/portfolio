import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove ALL aura/microdots blocks — every fragment from any past attempt
patterns_to_remove = [
    r'/\* Dot Matrix - Aura Background \*/.*?(?=\n/\* [A-Z]|\Z)',
    r'/\* Microdots - Aura Background \*/.*?(?=\n/\* [A-Z]|\Z)',
    r'/\* Dot Matrix - Aura \*/.*?(?=\n/\* [A-Z]|\Z)',
    r'/\* Microdots - Aura \*/.*?(?=\n/\* [A-Z]|\Z)',
    # Orphan layer blocks left behind
    r'/\* Layer 1 - (?:Microdot|Dot|normal).*?(?=\n/\* [A-Z]|\Z)',
    r'/\* Layer 2 - .*?(?=\n/\* [A-Z]|\Z)',
    r'/\* Layer 3 - .*?(?=\n/\* [A-Z]|\Z)',
    # The aura-bg, aura-layer-x blocks themselves (any remaining)
    r'\.aura-bg\s*\{[^}]+\}',
    r'\.aura-layer-1\s*\{[^}]+\}',
    r'\.aura-layer-2\s*\{[^}]+\}',
    r'\.aura-layer-3\s*\{[^}]+\}',
    # media queries for aura layers
    r'@media \(max-width: 768px\) \{\s*\.aura-layer-2[^}]+\}\s*\.aura-layer-3[^}]+\}\s*\}',
    # Ensure sections transparency block from old attempts
    r'/\* Ensure all page sections sit above aura.*?(?=\n/\*|\Z)',
    r'/\* Translucent Card.*?(?=\n/\*|\Z)',
    r'\.service-card:hover \+ \* \{[^}]+\}',
]

for pattern in patterns_to_remove:
    css = re.sub(pattern, '', css, flags=re.DOTALL)

# Also fix body background-color to #100e0b 
css = re.sub(r'--bg-color:\s*#[0-9a-fA-F]+;', '--bg-color: #100e0b;', css)
css = re.sub(r'background-color:\s*#[0-9a-fA-F]+ !important;\s*\}', '', css)

# Clean up excessive blank lines
css = re.sub(r'\n{4,}', '\n\n\n', css)

# Append the single clean Microdots block at end
microdots_clean = """

/* ─── Microdots Aura Background ──────────────────────────── */
/* Body base: blend modes composite against this color        */
body {
  background-color: #100e0b;
}

/* Fixed full-page aura — sits behind everything at z-index 0 */
.aura-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

/* Layer 1 — fine dot lattice, blend-mode: normal */
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

/* Layer 2 — central blue ellipse glow, blend-mode: screen */
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

/* Layer 3 — top-right sky blue accent, blend-mode: screen */
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

/* Mobile: reduce blur radius */
@media (max-width: 768px) {
  .aura-layer-2 { filter: blur(163px); }
  .aura-layer-3 { filter: blur(113px); }
}

/* Sections sit above the fixed aura (z-index 2) */
.navbar,
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

/* Cards: semi-transparent so dot grid shows through */
.service-card   { background: rgba(10,10,18,0.7)  !important; backdrop-filter: blur(12px); }
.project-card   { background: rgba(10,10,18,0.7)  !important; backdrop-filter: blur(12px); }
.blog-card      { background: rgba(10,10,18,0.7)  !important; backdrop-filter: blur(12px); }
.logo-panel     { background: rgba(10,10,18,0.5)  !important; backdrop-filter: blur(8px);  }
.contact-box    { background: rgba(10,10,18,0.7)  !important; backdrop-filter: blur(12px); }
/* ─────────────────────────────────────────────────────────── */
"""

css = css.rstrip() + '\n' + microdots_clean

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Verify
with open('styles.css', 'r', encoding='utf-8') as f:
    final = f.read()
count = final.count('.aura-layer-1')
print(f"aura-layer-1 occurrences in final file: {count}")
print("Done." if count == 1 else "WARNING: still duplicates!")
