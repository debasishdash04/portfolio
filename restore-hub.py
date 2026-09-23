import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the SVG in integrations-3d-hub with the Spline model
pattern = r'(<div class="integrations-3d-hub"[^>]*>)\s*<svg.*?</svg>\s*(</div>)'
replacement = r'\1\n        <div class="spline-lazy" data-spline-url="https://prod.spline.design/UmxwcPg2PfQWeMK3syNkSLvt-0f0/scene.splinecode" style="width: 100%; height: 100%; min-height: 350px;"></div>\n      \2'

html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
