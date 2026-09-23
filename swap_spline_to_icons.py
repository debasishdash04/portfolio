import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Card 1: Replace spline with animated floating frontend logos
card1_spline = '''        <div class="card-accent-bar"></div>
        <div class="card-spline-container">
          <div class="spline-lazy" data-spline-url="https://prod.spline.design/PAsbtQBA3-2Aywo4/scene.splinecode" style="width: 100%; height: 100%;"></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-laptop-code"></i></div>
          <h3>MODERN FRONTENDS</h3>'''

card1_new = '''        <div class="card-accent-bar"></div>
        <div class="card-float-icons">
          <div class="fi fi-1"><i class="fa-brands fa-react" style="color:#61dafb;"></i></div>
          <div class="fi fi-2"><i class="fa-brands fa-js" style="color:#f7df1e;"></i></div>
          <div class="fi fi-3"><i class="fa-brands fa-css3-alt" style="color:#264de4;"></i></div>
          <div class="fi fi-4"><i class="fa-brands fa-html5" style="color:#e34f26;"></i></div>
          <div class="fi fi-5"><i class="fa-brands fa-vuejs" style="color:#42b883;"></i></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-laptop-code"></i></div>
          <h3>MODERN FRONTENDS</h3>'''

# Card 2: Replace spline with animated security/backend logos
card2_spline = '''        <div class="card-accent-bar"></div>
        <div class="card-spline-container">
          <div class="spline-lazy" data-spline-url="https://prod.spline.design/FLbJ25JVu9aE4wKh/scene.splinecode" style="width: 100%; height: 100%;"></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-shield-halved"></i></div>
          <h3>ULTRA-SECURE BACKENDS <span class="card-arrow">&rarr;</span></h3>'''

card2_new = '''        <div class="card-accent-bar"></div>
        <div class="card-float-icons">
          <div class="fi fi-1"><i class="fa-brands fa-node-js" style="color:#68a063;"></i></div>
          <div class="fi fi-2"><i class="fa-brands fa-python" style="color:#3776ab;"></i></div>
          <div class="fi fi-3"><i class="fa-solid fa-database" style="color:#336791;"></i></div>
          <div class="fi fi-4"><i class="fa-brands fa-docker" style="color:#0db7ed;"></i></div>
          <div class="fi fi-5"><i class="fa-solid fa-server" style="color:#00e5ff;"></i></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-shield-halved"></i></div>
          <h3>ULTRA-SECURE BACKENDS <span class="card-arrow">&rarr;</span></h3>'''

# Card 3: Replace spline with animated automation logos
card3_spline = '''        <div class="card-accent-bar"></div>
        <div class="card-spline-container">
          <div class="spline-lazy" data-spline-url="https://prod.spline.design/O-lETJiYMdFUpobz/scene.splinecode" style="width: 100%; height: 100%;"></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-bolt"></i></div>
          <h3>BUSINESS AUTOMATION</h3>'''

card3_new = '''        <div class="card-accent-bar"></div>
        <div class="card-float-icons">
          <div class="fi fi-1"><i class="fa-solid fa-robot" style="color:#00e5ff;"></i></div>
          <div class="fi fi-2"><i class="fa-solid fa-gear" style="color:#a78bfa;"></i></div>
          <div class="fi fi-3"><i class="fa-solid fa-bolt" style="color:#fbbf24;"></i></div>
          <div class="fi fi-4"><i class="fa-solid fa-cloud" style="color:#38bdf8;"></i></div>
          <div class="fi fi-5"><i class="fa-solid fa-diagram-project" style="color:#34d399;"></i></div>
        </div>
        <div class="card-content">
          <div class="card-icon-wrap"><i class="fa-solid fa-bolt"></i></div>
          <h3>BUSINESS AUTOMATION</h3>'''

html = html.replace(card1_spline, card1_new)
html = html.replace(card2_spline, card2_new)
html = html.replace(card3_spline, card3_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Replaced Spline containers with floating icon animations in cards 1, 2, 3")
