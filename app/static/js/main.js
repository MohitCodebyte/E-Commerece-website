/**
 * NOVA MART — Premium Motion, Scroll Animation & Interaction Controller
 * Pure Vanilla JavaScript | IntersectionObserver | Zero Framework Dependencies
 */

document.addEventListener('DOMContentLoaded', () => {
  initPageEntrance();
  initScrollReveal();
  initHeaderScroll();
  initScrollProgress();
  initHeroMicroParallax();
  initToasts();
  initWishlistToggles();
  initCartForms();
  initModals();
  initKpiCounters();
});

// --- 1. Global Page Entrance ---
function initPageEntrance() {
  const main = document.querySelector('main');
  if (main) {
    main.classList.add('page-enter-active');
  }
}

// --- 2. IntersectionObserver Scroll Reveal Engine ---
function initScrollReveal() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-left, .reveal-right, .reveal-scale, .stagger-container');
  
  revealElements.forEach(el => {
    el.classList.add('reveal-init');
  });

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.1
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // If it's a staggered container, stagger its direct children
        if (entry.target.classList.contains('stagger-container')) {
          const children = entry.target.children;
          Array.from(children).forEach((child, index) => {
            child.style.transitionDelay = `${index * 60}ms`;
          });
        }
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach(el => revealObserver.observe(el));
}

// --- 3. Reactive Header on Scroll ---
function initHeaderScroll() {
  const header = document.querySelector('.nav-sticky-header') || document.querySelector('header');
  if (!header) return;

  let ticking = false;

  function updateHeader() {
    if (window.scrollY > 20) {
      header.classList.add('header-scrolled');
    } else {
      header.classList.remove('header-scrolled');
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });

  updateHeader();
}

// --- 4. Top Scroll Progress Indicator ---
function initScrollProgress() {
  const progressBar = document.getElementById('scroll-progress');
  if (!progressBar) return;

  let ticking = false;

  function updateProgress() {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight > 0) {
      const scrollPercent = (window.scrollY / docHeight) * 100;
      progressBar.style.width = `${Math.min(scrollPercent, 100)}%`;
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateProgress);
      ticking = true;
    }
  }, { passive: true });
}

// --- 5. Hero Showcase Image Micro-Parallax (Desktop Only) ---
function initHeroMicroParallax() {
  if (window.innerWidth < 1024 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const heroShowcase = document.getElementById('hero-showcase-image');
  if (!heroShowcase) return;

  let ticking = false;

  function applyParallax() {
    if (window.scrollY < 600) {
      const offset = window.scrollY * 0.05; // Maximum 10-15px subtle shift
      heroShowcase.style.transform = `translateY(${offset}px)`;
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(applyParallax);
      ticking = true;
    }
  }, { passive: true });
}

// --- 6. Global Toast System ---
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const iconName = type === 'success' ? 'check_circle' : type === 'error' ? 'error' : type === 'warning' ? 'warning' : 'info';
  toast.innerHTML = `
    <span class="material-symbols-outlined text-xl">${iconName}</span>
    <div class="flex-1">${message}</div>
    <button type="button" class="text-white/60 hover:text-white ml-2 text-sm" onclick="this.parentElement.remove()" title="Close">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

function initToasts() {
  const flashed = document.querySelectorAll('.flash-message-item');
  flashed.forEach(item => {
    const text = item.getAttribute('data-message');
    const type = item.getAttribute('data-type') || 'info';
    if (text) showToast(text, type);
  });
}

// --- 7. Wishlist Interaction with Smooth Pulse ---
function initWishlistToggles() {
  document.querySelectorAll('.wishlist-toggle-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const productId = btn.getAttribute('data-product-id');
      if (!productId) return;

      try {
        const formData = new FormData();
        formData.append('product_id', productId);

        const res = await fetch('/wishlist/toggle', {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        
        if (data.success) {
          const icon = btn.querySelector('.material-symbols-outlined');
          if (icon) {
            btn.classList.add('animate-heart-pop');
            setTimeout(() => btn.classList.remove('animate-heart-pop'), 350);

            if (data.in_wishlist) {
              icon.classList.add('fill', 'text-rose-500');
              icon.style.fontVariationSettings = "'FILL' 1";
              showToast('Added to your wishlist', 'success');
            } else {
              icon.classList.remove('fill', 'text-rose-500');
              icon.style.fontVariationSettings = "'FILL' 0";
              showToast('Removed from wishlist', 'info');
            }
          }
          // Update global wishlist badge
          const badge = document.querySelector('.wishlist-count-badge');
          if (badge && data.wishlist_count !== undefined) {
            badge.textContent = data.wishlist_count;
            badge.classList.toggle('hidden', data.wishlist_count === 0);
            badge.classList.add('animate-badge-bump');
            setTimeout(() => badge.classList.remove('animate-badge-bump'), 300);
          }
        }
      } catch (err) {
        console.error('Wishlist toggle error:', err);
      }
    });
  });
}

// --- 8. Add to Cart Multi-State Feedback & Badge Pop ---
function initCartForms() {
  document.querySelectorAll('.ajax-add-to-cart').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalHTML = submitBtn ? submitBtn.innerHTML : '';
      const originalBg = submitBtn ? submitBtn.className : '';

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin text-sm">progress_activity</span> <span>Adding...</span>';
      }

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        if (data.success) {
          showToast('Added to your shopping bag!', 'success');
          
          // Button Multi-State Success Feedback
          if (submitBtn) {
            submitBtn.className = submitBtn.className.replace('bg-slate-900', 'bg-emerald-600').replace('hover:bg-indigo-600', 'bg-emerald-600');
            submitBtn.innerHTML = '<span class="material-symbols-outlined text-sm">check_circle</span> <span>Added ✓</span>';
            setTimeout(() => {
              submitBtn.className = originalBg;
              submitBtn.innerHTML = originalHTML;
              submitBtn.disabled = false;
            }, 1200);
          }

          // Cart badge bump update
          const badges = document.querySelectorAll('.cart-count-badge');
          badges.forEach(b => {
            b.textContent = data.cart.item_count;
            b.classList.toggle('hidden', data.cart.item_count === 0);
            b.classList.add('animate-badge-bump');
            setTimeout(() => b.classList.remove('animate-badge-bump'), 300);
          });
        }
      } catch (err) {
        form.submit(); // fallback to normal submit if ajax fails
      }
    });
  });
}

// --- 9. Modals & Drawers with Body Scroll Lock ---
function initModals() {
  document.querySelectorAll('[data-modal-target]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.getAttribute('data-modal-target');
      const modal = document.getElementById(targetId);
      if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  document.querySelectorAll('[data-modal-close]').forEach(closer => {
    closer.addEventListener('click', () => {
      const modal = closer.closest('.modal-container') || closer.closest('.fixed');
      if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }
    });
  });
}

// --- 10. Single-Run Dashboard KPI Number Counter ---
function initKpiCounters() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const kpiElements = document.querySelectorAll('.kpi-counter');
  if (kpiElements.length === 0) return;

  const kpiObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseFloat(el.getAttribute('data-target') || el.innerText.replace(/[^0-9.]/g, ''));
        if (!isNaN(target)) {
          let start = 0;
          const duration = 750;
          const startTime = performance.now();

          function updateNumber(time) {
            const elapsed = time - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease-out cubic
            const current = Math.floor(start + (target - start) * (1 - Math.pow(1 - progress, 3)));
            
            const prefix = el.getAttribute('data-prefix') || '';
            el.innerText = prefix + current.toLocaleString('en-IN');

            if (progress < 1) {
              requestAnimationFrame(updateNumber);
            }
          }
          requestAnimationFrame(updateNumber);
        }
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });

  kpiElements.forEach(el => kpiObserver.observe(el));
}
