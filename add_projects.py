import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add PROJECTS to Navbar
if 'href="#projects"' not in html:
    html = html.replace('<li><a href="#services">SERVICES</a></li>', '<li><a href="#services">SERVICES</a></li>\n      <li><a href="#projects">PROJECTS</a></li>')

# 2. Insert Projects Section
projects_html = """
  <!-- Featured Projects Showcase Section -->
  <section id="projects" class="projects-section">
    <h2 class="section-title">FEATURED PROJECTS</h2>
    <div class="projects-grid">
      
      <!-- Project Card 1 -->
      <article class="project-card">
        <div class="project-preview-box">
          <div class="project-preview-overlay">
            <span class="project-kicker">AI &amp; FULL-STACK</span>
            <div class="project-preview-badge"><i class="fa-solid fa-bolt"></i> LIVE SYSTEM</div>
          </div>
          <div class="project-visual-graphic">
            <div class="code-header">
              <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
              <span class="code-title">apex-ai-core.py</span>
            </div>
            <pre class="code-snippet"><code><span class="code-keyword">async def</span> <span class="code-func">process_query</span>(prompt: str):
  pipeline = RAGPipeline(model=<span class="code-str">"claude-3.5"</span>)
  <span class="code-keyword">return await</span> pipeline.execute(prompt)</code></pre>
          </div>
        </div>
        <div class="project-details">
          <h3 class="project-title">Apex AI SaaS Platform</h3>
          <p class="project-desc">Intelligent analytics dashboard featuring real-time LLM query processing, RAG pipelines, and automated reporting workflows.</p>
          <div class="project-tags">
            <span class="project-tag">React 19</span>
            <span class="project-tag">FastAPI</span>
            <span class="project-tag">LangChain</span>
            <span class="project-tag">PostgreSQL</span>
            <span class="project-tag">Tailwind</span>
          </div>
          <div class="project-links">
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn primary">// VIEW DEMO <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn secondary"><i class="fa-brands fa-github"></i> REPO</a>
          </div>
        </div>
      </article>

      <!-- Project Card 2 -->
      <article class="project-card">
        <div class="project-preview-box fintech">
          <div class="project-preview-overlay">
            <span class="project-kicker">FINTECH &amp; AUTOMATION</span>
            <div class="project-preview-badge"><i class="fa-solid fa-shield-halved"></i> SECURE GATEWAY</div>
          </div>
          <div class="project-visual-graphic">
            <div class="code-header">
              <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
              <span class="code-title">omnipay-webhook.js</span>
            </div>
            <pre class="code-snippet"><code><span class="code-keyword">const</span> stripe = <span class="code-func">require</span>(<span class="code-str">'stripe'</span>)(KEY);
app.<span class="code-func">post</span>(<span class="code-str">'/webhook'</span>, <span class="code-keyword">async</span> (req, res) => {
  <span class="code-keyword">await</span> paymentService.<span class="code-func">verifyAndRoute</span>(req);
});</code></pre>
          </div>
        </div>
        <div class="project-details">
          <h3 class="project-title">OmniPay Global Checkout</h3>
          <p class="project-desc">Ultra-fast global payment gateway with automated webhooks, Stripe/PayPal integration, and multi-currency transaction routing.</p>
          <div class="project-tags">
            <span class="project-tag">Node.js</span>
            <span class="project-tag">Express</span>
            <span class="project-tag">Stripe API</span>
            <span class="project-tag">Redis</span>
            <span class="project-tag">Docker</span>
          </div>
          <div class="project-links">
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn primary">// VIEW DEMO <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn secondary"><i class="fa-brands fa-github"></i> REPO</a>
          </div>
        </div>
      </article>

      <!-- Project Card 3 -->
      <article class="project-card">
        <div class="project-preview-box security">
          <div class="project-preview-overlay">
            <span class="project-kicker">CLOUD &amp; SECURITY</span>
            <div class="project-preview-badge"><i class="fa-solid fa-server"></i> INFRASTRUCTURE</div>
          </div>
          <div class="project-visual-graphic">
            <div class="code-header">
              <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
              <span class="code-title">cybervault-cluster.yml</span>
            </div>
            <pre class="code-snippet"><code><span class="code-keyword">services</span>:
  <span class="code-func">api</span>:
    <span class="code-keyword">image</span>: cybervault/core:latest
    <span class="code-keyword">deploy</span>: { <span class="code-str">replicas</span>: 8 }</code></pre>
          </div>
        </div>
        <div class="project-details">
          <h3 class="project-title">CyberVault Cloud Manager</h3>
          <p class="project-desc">High-security cloud infrastructure management portal with role-based access control, live cluster metrics, and automated backups.</p>
          <div class="project-tags">
            <span class="project-tag">Svelte</span>
            <span class="project-tag">Django</span>
            <span class="project-tag">Docker</span>
            <span class="project-tag">PostgreSQL</span>
            <span class="project-tag">Tailwind</span>
          </div>
          <div class="project-links">
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn primary">// VIEW DEMO <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
            <a href="https://github.com/debasishdash04" target="_blank" rel="noopener noreferrer" class="project-btn secondary"><i class="fa-brands fa-github"></i> REPO</a>
          </div>
        </div>
      </article>

    </div>
  </section>
"""

if 'id="projects"' not in html:
    html = html.replace('</section>\n\n  <!-- Integrations / Tech Stack Section -->', '</section>\n' + projects_html + '\n  <!-- Integrations / Tech Stack Section -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully")
