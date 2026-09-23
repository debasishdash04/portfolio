projects_css = """

/* Projects Section Styling */
.projects-section {
  padding: 6rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 4rem;
  z-index: 10;
  position: relative;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.project-card {
  background: rgba(15, 15, 15, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.project-card:hover {
  transform: translateY(-8px);
  border-color: rgba(0, 229, 255, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 229, 255, 0.15);
}

.project-preview-box {
  position: relative;
  background: linear-gradient(135deg, #0b1528 0%, #050a12 100%);
  padding: 1.5rem;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.project-preview-box.fintech {
  background: linear-gradient(135deg, #120b28 0%, #050512 100%);
}

.project-preview-box.security {
  background: linear-gradient(135deg, #0b281f 0%, #05120d 100%);
}

.project-preview-overlay {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.project-kicker {
  font-size: 0.75rem;
  letter-spacing: 2px;
  font-weight: 700;
  color: #00e5ff;
}

.project-preview-badge {
  font-size: 0.7rem;
  letter-spacing: 1px;
  font-weight: 600;
  padding: 0.3rem 0.8rem;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: 100px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.project-visual-graphic {
  background: rgba(5, 5, 5, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 1rem;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 0.8rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
}

.code-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.code-title {
  font-size: 0.75rem;
  color: #888;
  margin-left: 0.4rem;
}

.code-snippet {
  margin: 0;
  color: #d1d5db;
  line-height: 1.5;
  white-space: pre-wrap;
}

.code-keyword { color: #ff79c6; font-weight: 600; }
.code-func { color: #50fa7b; }
.code-str { color: #f1fa8c; }

.project-details {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex-grow: 1;
}

.project-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.project-desc {
  color: #a0aec0;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.project-tag {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.35rem 0.8rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  color: #e2e8f0;
  transition: all 0.3s ease;
}

.project-card:hover .project-tag {
  border-color: rgba(0, 229, 255, 0.2);
  background: rgba(0, 229, 255, 0.05);
}

.project-links {
  display: flex;
  gap: 1rem;
  margin-top: auto;
  padding-top: 0.75rem;
}

.project-btn {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0.75rem 1.4rem;
  border-radius: 8px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.project-btn.primary {
  background: rgba(0, 229, 255, 0.1);
  color: #00e5ff;
  border: 1px solid rgba(0, 229, 255, 0.4);
}

.project-btn.primary:hover {
  background: #00e5ff;
  color: #050505;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
}

.project-btn.secondary {
  background: rgba(255, 255, 255, 0.03);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.project-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}
"""

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.projects-section' not in css:
    with open('styles.css', 'a', encoding='utf-8') as f:
        f.write(projects_css)
    print("Appended projects CSS successfully")
else:
    print("Projects CSS already exists")
