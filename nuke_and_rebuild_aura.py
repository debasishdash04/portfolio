import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# ── Step 1: Nuke every aura/microdot/dot-matrix fragment ──
# Remove any block starting with aura-related comments
css = re.sub(r'/\*.*?(?:Microdots|Dot Matrix|Aura|aura).*?\*/.*?(?=\n/\*\s[A-Z]|\Z)', '', css, flags=re.DOTALL)

# Remove any standalone .aura-* rule blocks
css = re.sub(r'\.aura-(?:bg|layer-[123])\s*\{[^}]*\}', '', css)

# Remove orphan body { background-color: #100e0b; } or !important blocks left behind
css = re.sub(r'body\s*\{\s*background-color:\s*#100e0b[^}]*\}', '', css)

# Remove any card !important overrides from old aura attempts
css = re.sub(r'\.service-card\s*\{[^}]*!important[^}]*\}', '', css)
css = re.sub(r'\.project-card\s*\{[^}]*!important[^}]*\}', '', css)
css = re.sub(r'\.blog-card\s*\{[^}]*!important[^}]*\}', '', css)
css = re.sub(r'\.logo-panel\s*\{[^}]*!important[^}]*\}', '', css)
css = re.sub(r'\.contact-box\s*\{[^}]*!important[^}]*\}', '', css)

# Remove orphaned @media blocks for aura layers
css = re.sub(r'@media\s*\(max-width:\s*768px\)\s*\{\s*\.aura-layer-[23][^}]*\}(?:\s*\.aura-layer-[23][^}]*\})?\s*\}', '', css)

# Remove section z-index overrides from aura attempts
css = re.sub(r'/\*\s*(?:Sections sit|All sections|Ensure all).*?\*/\s*(?:\.(?:navbar|hero|services|projects|integrations|blog|contact|industries|dashboard|cta|footer)[^{]*,?\s*)+\{[^}]*\}', '', css, flags=re.DOTALL)

# Remove any line with just "backdrop-filter" and "!important" on cards
for sel in ['.service-card', '.project-card', '.blog-card', '.logo-panel', '.contact-box']:
    escaped = re.escape(sel)
    css = re.sub(escaped + r'\s*\{[^}]*!important[^}]*\}', '', css)

# Clean excessive blank lines
css = re.sub(r'\n{3,}', '\n\n', css)

# ── Step 2: Fix the body rule at the top ──
# Make sure body has background-color: #100e0b (no !important)
css = re.sub(
    r'(body\s*\{)\s*background-color:[^;]+;',
    r'\1\n  background-color: #100e0b;',
    css,
    count=1
)

# Fix --bg-color to match
css = re.sub(r'--bg-color:\s*[^;]+;', '--bg-color: #100e0b;', css)

# ── Step 3: Append one clean Microdots block ──
microdots = """

/* ── Microdots Aura Background ──────────────────────────── */
.aura-bg {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

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

/* Sections above aura */
.navbar          { z-index: 100; }
.hero            { position: relative; z-index: 2; }
.services-section { position: relative; z-index: 2; }
.projects-section { position: relative; z-index: 2; }
.integrations-section { position: relative; z-index: 2; }
.blog-section    { position: relative; z-index: 2; }
.contact-section { position: relative; z-index: 2; }
footer           { position: relative; z-index: 2; }
/* ────────────────────────────────────────────────────────── */
"""

css = css.rstrip() + '\n' + microdots

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# ── Verify ──
with open('styles.css', 'r', encoding='utf-8') as f:
    final = f.read()

checks = {
    '.aura-layer-1': final.count('.aura-layer-1'),
    '.aura-layer-2': final.count('.aura-layer-2'),
    '.aura-layer-3': final.count('.aura-layer-3'),
    '.aura-bg': final.count('.aura-bg'),
    '!important': final.count('!important'),
    '#050505': final.count('#050505'),
}
for k, v in checks.items():
    status = 'OK' if (v <= 2 if k in ['.aura-layer-2','.aura-layer-3'] else v <= 1) else 'WARN'
    if k == '!important':
        status = 'OK' if v <= 5 else f'WARN({v})'
    if k == '#050505':
        status = 'OK' if v == 0 else f'WARN({v})'
    print(f"  {k}: {v} ({status})")

print("Done.")
