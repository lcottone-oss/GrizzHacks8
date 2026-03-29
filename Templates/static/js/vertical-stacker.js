/**
 * ============================================================
 * VERTICAL STACKER - Scroll Pinning & Reveal Effects
 * ============================================================
 */

class VerticalStacker {
  constructor() {
    this.slabs = document.querySelectorAll('.stacker-slab');
    this.observerOptions = {
      threshold: [0, 0.1, 0.25, 0.5, 0.75],
      rootMargin: '-70px 0px -100px 0px'
    };
    this.init();
  }

  init() {
    if (!this.slabs.length) return;

    // Intersection Observer for reveal effects
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.1) {
          entry.target.classList.add('is-visible');
          this.triggerRevealAnimation(entry.target);
        }
      });
    }, this.observerOptions);

    this.slabs.forEach((slab) => {
      this.observer.observe(slab);
    });

    // Handle scroll for pinning effect
    window.addEventListener('scroll', () => this.handleScroll(), { passive: true });
    
    // Initial check
    this.handleScroll();
  }

  handleScroll() {
    const navHeight = 70;
    
    this.slabs.forEach((slab, index) => {
      const rect = slab.getBoundingClientRect();

      // Check if slab is in viewport top
      if (rect.top <= navHeight && rect.bottom > navHeight) {
        slab.classList.add('is-pinned');
      } else {
        slab.classList.remove('is-pinned');
      }
    });
  }

  triggerRevealAnimation(element) {
    const maskShape = element.querySelector('.reveal-mask-shape');
    if (maskShape && !maskShape.hasAttribute('data-animated')) {
      maskShape.setAttribute('data-animated', 'true');
      
      // Force reflow to restart animation
      void maskShape.offsetHeight;
      maskShape.style.animation = 'none';
      
      setTimeout(() => {
        maskShape.style.animation = 'reveal-slide-out 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards';
      }, 10);
    }
  }

  destroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new VerticalStacker();
  });
} else {
  new VerticalStacker();
}
