import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace plain checkmark character with styled FontAwesome check icon
html = html.replace('<li>✓ ', '<li><i class="fa-solid fa-check" style="color: #00e5ff; font-size: 0.85rem; margin-right: 6px;"></i> ')

# Add sleek icons to all card titles
card_icons = {
    '<h3 style="color: #00e5ff;">FRONTENDS</h3>': '<h3 style="color: #00e5ff;"><i class="fa-solid fa-laptop-code" style="margin-right: 8px;"></i> FRONTENDS</h3>',
    '<h3 style="color: #00e5ff;">AUTOMATION</h3>': '<h3 style="color: #00e5ff;"><i class="fa-solid fa-bolt" style="margin-right: 8px;"></i> AUTOMATION</h3>',
    '<h3 style="color: #00e5ff;">SAAS DASHBOARDS</h3>': '<h3 style="color: #00e5ff;"><i class="fa-solid fa-chart-line" style="margin-right: 8px;"></i> SAAS DASHBOARDS</h3>',
    '<h3 style="color: #00e5ff;">PAYMENT GATEWAYS</h3>': '<h3 style="color: #00e5ff;"><i class="fa-solid fa-credit-card" style="margin-right: 8px;"></i> PAYMENT GATEWAYS</h3>',
    '<h3 style="color: #00e5ff;">AI INTEGRATIONS</h3>': '<h3 style="color: #00e5ff;"><i class="fa-solid fa-brain" style="margin-right: 8px;"></i> AI INTEGRATIONS</h3>'
}

for old, new in card_icons.items():
    html = html.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
