import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

classes = set(re.findall(r'class="([^"]+)"', html))
all_cls = set()
for c in classes:
    for part in c.split():
        all_cls.add(part)

missing = []
for c in sorted(all_cls):
    if c not in css and not c.startswith('fa-') and not c.startswith('scroll-'):
        missing.append(c)

print("Classes in HTML not found in CSS:")
for m in missing:
    print("  " + m)
print("Total HTML classes:", len(all_cls), "Missing:", len(missing))
print("CSS file lines:", css.count("\n"))
