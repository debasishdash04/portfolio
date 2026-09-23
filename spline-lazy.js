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

  // Low-end / mobile: skip ALL Spline WebGL to save CPU & battery
  const isLowEnd = window.innerWidth < 768 || navigator.hardwareConcurrency <= 2;

  if (isLowEnd) {
    const splineContainer = document.querySelector('.spline-container');
    const splineFallback  = document.getElementById('spline-fallback');
    if (splineContainer) splineContainer.style.display = 'none';
    if (splineFallback)  splineFallback.style.display  = 'block';
    // Don't observe lazy cards on low-end at all
  } else {
    document.querySelectorAll('.spline-lazy').forEach(el => splineObserver.observe(el));

    // Fallback: show hero image if Spline hasn't started in 8s
    setTimeout(() => {
      const heroViewer = document.querySelector('.spline-container spline-viewer');
      if (!heroViewer || !heroViewer.shadowRoot) {
        const fallback = document.getElementById('spline-fallback');
        if (fallback) fallback.style.display = 'block';
      }
    }, 8000);
  }
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
