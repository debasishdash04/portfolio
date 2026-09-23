import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restore Hero Spline
html = re.sub(
    r'(<div class="spline-container">\s*)(<img src="assets/hero.png".*?>)(\s*</div>)',
    r'\1<div id="spline-fallback" style="display:none;">\2</div>\n      <spline-viewer url="https://prod.spline.design/msm-93IVk4kpllcY/scene.splinecode" background="transparent" style="width: 100%; height: 100%;"></spline-viewer>\3',
    html,
    flags=re.DOTALL
)

# 2. Map cards to their spline URLs
spline_map = {
    'FRONTENDS': 'https://prod.spline.design/PAsbtQBA3-2Aywo4/scene.splinecode',
    'SECURE BACKENDS': 'https://prod.spline.design/FLbJ25JVu9aE4wKh/scene.splinecode',
    'AUTOMATION': 'https://prod.spline.design/O-lETJiYMdFUpobz/scene.splinecode',
    'SAAS DASHBOARDS': '',
    'PAYMENT GATEWAYS': '',
    'AI INTEGRATIONS': ''
}

# 3. Add spline containers to cards
for title, url in spline_map.items():
    if url:
        container_html = f'<div class="card-spline-container">\n          <div class="spline-lazy" data-spline-url="{url}" style="width: 100%; height: 100%;"></div>\n        </div>\n        <div class="card-content"'
    else:
        container_html = f'<div class="card-spline-container">\n          <!-- Add Spline URL here later -->\n        </div>\n        <div class="card-content"'
    
    html = re.sub(
        rf'(<!-- Card \d+: {title} -->\s*<div class="service-card">\s*)<div class="card-content"',
        rf'\1{container_html}',
        html,
        flags=re.DOTALL
    )

# 4. Inject script at the bottom
if 'spline-lazy.js' not in html:
    html = html.replace('</body>', '  <script src="spline-lazy.js" defer></script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
