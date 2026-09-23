with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Card 1 to MODERN FRONTENDS
html = html.replace(
    '<h3 style="color: #00e5ff;"><i class="fa-solid fa-laptop-code" style="margin-right: 8px;"></i> FRONTENDS</h3>',
    '<h3 style="color: #00e5ff;"><i class="fa-solid fa-laptop-code" style="margin-right: 8px;"></i> MODERN FRONTENDS</h3>'
)

# Update Card 3 to BUSINESS AUTOMATION
html = html.replace(
    '<h3 style="color: #00e5ff;"><i class="fa-solid fa-bolt" style="margin-right: 8px;"></i> AUTOMATION</h3>',
    '<h3 style="color: #00e5ff;"><i class="fa-solid fa-bolt" style="margin-right: 8px;"></i> BUSINESS AUTOMATION</h3>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated titles for Card 1 and Card 3 in index.html")
