import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Append Modal HTML if not exists
modal_html = """
  <!-- Modal Overlay System -->
  <div class="modal-overlay" id="backend-modal">
    <div class="modal-container">
      <button class="modal-close" onclick="closeModal('backend-modal')">&times;</button>
      
      <div class="modal-header">
        <span class="modal-kicker">USE CASES</span>
        <h2 class="modal-title">What Can You Build?</h2>
        <p class="modal-subtitle">Cloud Functions power critical backend logic across industries.</p>
      </div>
      
      <div class="modal-grid">
        <!-- 1 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
          </div>
          <div class="uc-content">
            <h4>Data Validation</h4>
            <p>Enforce business rules server-side. Validate inputs, check constraints, and reject invalid data before it's saved.</p>
          </div>
        </div>
        <!-- 2 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          </div>
          <div class="uc-content">
            <h4>Payment Processing</h4>
            <p>Integrate with Stripe, PayPal, or other processors. Handle webhooks, validate payments, update order status.</p>
          </div>
        </div>
        <!-- 3 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <div class="uc-content">
            <h4>Email Notifications</h4>
            <p>Send transactional emails on data changes. Welcome emails, order confirmations, password resets.</p>
          </div>
        </div>
        <!-- 4 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
          </div>
          <div class="uc-content">
            <h4>Third-Party APIs</h4>
            <p>Connect to external services. Weather data, social media, analytics, AI services — all from your backend.</p>
          </div>
        </div>
        <!-- 5 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <div class="uc-content">
            <h4>Report Generation</h4>
            <p>Generate PDFs, spreadsheets, or data exports. Run as background jobs for large datasets.</p>
          </div>
        </div>
        <!-- 6 -->
        <div class="usecase-card">
          <div class="uc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
          </div>
          <div class="uc-content">
            <h4>Data Sync</h4>
            <p>Keep data in sync with external systems. CRM updates, inventory sync, analytics pipelines.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

if 'id="backend-modal"' not in html:
    html = html.replace('  <script src="spline-lazy.js" defer></script>', modal_html + '\n  <script src="spline-lazy.js" defer></script>')

# 2. Add onclick to SECURE BACKENDS card
# Locate the SECURE BACKENDS card content wrapper
pattern = r'(<!-- Card 2: SECURE BACKENDS -->\s*<div class="service-card">\s*<div class="card-spline-container">[\s\S]*?</div>\s*)<div class="card-content" style="max-width: 100%;">'
replacement = r'\1<div class="card-content" style="max-width: 100%; cursor: pointer;" onclick="openModal(\'backend-modal\')">'

if 'openModal(\'backend-modal\')' not in html:
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
