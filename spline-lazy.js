document.addEventListener("DOMContentLoaded", () => {
  // --- Spline 3D Lazy Loading (only when truly in viewport) ---
  const splineObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const container = entry.target;
      if (entry.isIntersecting) {
        if (!container.hasAttribute('data-loaded')) {
          container.setAttribute('data-loaded', 'true');
          const url = container.getAttribute('data-spline-url');
          if (url) {
            // Disable pointer events so it never blocks scroll
            container.innerHTML = `<spline-viewer url="${url}" background="transparent" events-target="none" style="width:100%; height:100%; pointer-events:none;"></spline-viewer>`;
          }
        }
      }
    });
  // Tight margin: only load when the card is nearly in view
  }, { rootMargin: '50px', threshold: 0.1 });

  // Observe all Spline lazy elements on both desktop and mobile
  document.querySelectorAll('.spline-lazy').forEach(el => splineObserver.observe(el));

  // Fallback: show hero image if Spline hasn't started in 8s
  setTimeout(() => {
    const heroViewer = document.querySelector('.spline-container spline-viewer');
    if (!heroViewer || !heroViewer.shadowRoot) {
      const fallback = document.getElementById('spline-fallback');
      if (fallback) fallback.style.display = 'block';
    }
  }, 8000);
});

// --- Modal System ---
window.openModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
};

window.closeModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
};

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const activeModal = document.querySelector('.modal-overlay.active');
    if (activeModal) window.closeModal(activeModal.id);
  }
});

// Close on backdrop click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    window.closeModal(e.target.id);
  }
});

// --- Offline Redirect (event-based only, no polling interval) ---
function handleOffline() {
  if (!window.location.pathname.endsWith('404.html')) {
    window.location.href = './404.html';
  }
}
window.addEventListener('offline', handleOffline);

// --- Showreel Video Play/Pause Toggle ---
window.toggleShowreel = function(btn) {
  const video = document.getElementById('showreel-video');
  if (!video) return;
  const icon = btn.querySelector('i');
  if (video.paused) {
    video.play();
    icon.className = 'fa-solid fa-pause';
    btn.setAttribute('aria-label', 'Pause video');
  } else {
    video.pause();
    icon.className = 'fa-solid fa-play';
    btn.setAttribute('aria-label', 'Play video');
  }
};

// --- "Get noticed." Scroll-Triggered Animated Orb ---
document.addEventListener("DOMContentLoaded", () => {
  const heading = document.getElementById('get-noticed-heading');
  const orb = document.getElementById('noticed-orb');
  const face = document.getElementById('orb-face');

  if (!heading || !orb || !face) return;

  // Scroll detection to wake up / sleep
  function checkOrbScroll() {
    const rect = heading.getBoundingClientRect();
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;

    // Wake up when within visible reading range
    if (rect.top < windowHeight * 0.88 && rect.bottom > windowHeight * 0.12) {
      if (!heading.classList.contains('awake')) {
        heading.classList.add('awake');
      }
    } else {
      if (heading.classList.contains('awake')) {
        heading.classList.remove('awake');
      }
    }
  }

  window.addEventListener('scroll', checkOrbScroll, { passive: true });
  window.addEventListener('resize', checkOrbScroll, { passive: true });
  checkOrbScroll();

  // Mouse tracking: eyes glance towards cursor when awake
  let ticking = false;
  window.addEventListener('mousemove', (e) => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        if (heading.classList.contains('awake')) {
          const orbRect = orb.getBoundingClientRect();
          const orbCenterX = orbRect.left + orbRect.width / 2;
          const orbCenterY = orbRect.top + orbRect.height / 2;

          const dx = e.clientX - orbCenterX;
          const dy = e.clientY - orbCenterY;
          const dist = Math.hypot(dx, dy);

          // Subtle parallax glance (max 6px offset)
          const maxOffset = 6;
          const angle = Math.atan2(dy, dx);
          const offsetDist = Math.min(maxOffset, dist * 0.015);

          const moveX = Math.cos(angle) * offsetDist;
          const moveY = Math.sin(angle) * offsetDist;

          face.style.transform = `translate(${moveX.toFixed(1)}px, ${moveY.toFixed(1)}px)`;
        } else {
          face.style.transform = 'translate(0px, 0px)';
        }
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Playful wink/blink on click or touch
  orb.addEventListener('click', () => {
    heading.classList.add('wink');
    setTimeout(() => {
      heading.classList.remove('wink');
    }, 320);
  });
});

// --- Live Clock in Navbar (Asia/Kolkata / IST) ---
document.addEventListener("DOMContentLoaded", () => {
  const clockEl = document.getElementById('local-time-clock');
  if (!clockEl) return;

  function updateClock() {
    try {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', {
        timeZone: 'Asia/Kolkata',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
      clockEl.textContent = timeStr;
    } catch (e) {
      const now = new Date();
      clockEl.textContent = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
    }
  }

  updateClock();
  setInterval(updateClock, 1000);
});

// --- FAQ Accordion Interactive Toggle ---
document.addEventListener("DOMContentLoaded", () => {
  const faqItems = document.querySelectorAll('.faq-item');
  if (!faqItems.length) return;

  faqItems.forEach(item => {
    const trigger = item.querySelector('.faq-trigger');
    if (!trigger) return;

    trigger.addEventListener('click', () => {
      const isActive = item.classList.contains('active');

      // Close other accordion items for clean UX
      faqItems.forEach(other => {
        if (other !== item) {
          other.classList.remove('active');
          const otherTrigger = other.querySelector('.faq-trigger');
          if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
        }
      });

      if (isActive) {
        item.classList.remove('active');
        trigger.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('active');
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
  });
});

// --- One-Click Copy Email & Toast Notification ---
document.addEventListener("DOMContentLoaded", () => {
  const toast = document.getElementById('toast-pill');
  const toastMsg = document.getElementById('toast-message');
  let toastTimer = null;

  function showToast(message) {
    if (!toast || !toastMsg) return;
    toastMsg.textContent = message;
    toast.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2400);
  }

  // Bind to copy buttons and email links
  document.querySelectorAll('.git-copy-btn, .git-inquiry-email').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const email = btn.getAttribute('data-email');
      if (email && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(email).then(() => {
          showToast(`Copied ${email} to clipboard!`);
        }).catch(() => {
          showToast(`Email: ${email}`);
        });
      }
    });
  });
});
