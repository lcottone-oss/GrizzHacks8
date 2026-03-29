/**
 * ============================================================
 * HORIZONTAL CAROUSEL - Draggable Filmstrip with Ripple
 * ============================================================
 */

class HorizontalCarousel {
  constructor() {
    this.filmstrips = document.querySelectorAll('.filmstrip');
    this.isDragging = false;
    this.startX = 0;
    this.scrollLeft = 0;
    this.velocity = 0;
    this.startTime = 0;
    this.init();
  }

  init() {
    if (!this.filmstrips.length) return;

    this.filmstrips.forEach((filmstrip) => {
      const container = filmstrip.parentElement;

      // Mouse events
      filmstrip.addEventListener('mousedown', (e) => this.handleDragStart(e, filmstrip, container));
      filmstrip.addEventListener('mouseleave', (e) => this.handleDragEnd(e, filmstrip, container));
      filmstrip.addEventListener('mouseup', (e) => this.handleDragEnd(e, filmstrip, container));
      filmstrip.addEventListener('mousemove', (e) => this.handleDrag(e, filmstrip));

      // Touch events for mobile
      filmstrip.addEventListener('touchstart', (e) => this.handleDragStart(e, filmstrip, container));
      filmstrip.addEventListener('touchend', (e) => this.handleDragEnd(e, filmstrip, container));
      filmstrip.addEventListener('touchmove', (e) => this.handleDrag(e, filmstrip));

      // Case card click
      const cards = filmstrip.querySelectorAll('.case-card');
      cards.forEach((card) => {
        card.addEventListener('click', (e) => {
          if (!this.isDragging) {
            this.triggerRippleEffect(card, e);
          }
        });
      });
    });
  }

  handleDragStart(e, filmstrip, container) {
    this.isDragging = true;
    this.startX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
    this.scrollLeft = filmstrip.scrollLeft;
    this.startTime = Date.now();
    container.classList.add('is-dragging');
    e.preventDefault();
  }

  handleDrag(e, filmstrip) {
    if (!this.isDragging) return;

    const x = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
    const walk = (this.startX - x) * 1.5; // Multiplier for smoother drag
    this.velocity = walk * 0.3;

    filmstrip.scrollLeft = this.scrollLeft + walk;
  }

  handleDragEnd(e, filmstrip, container) {
    if (!this.isDragging) return;

    this.isDragging = false;
    container.classList.remove('is-dragging');

    // Calculate momentum
    const elapsed = Date.now() - this.startTime;
    const currentVelocity = this.velocity * (elapsed > 100 ? 0.8 : 1);

    // Momentum scrolling with deceleration
    if (Math.abs(currentVelocity) > 0.5) {
      this.applyMomentumScroll(filmstrip, currentVelocity);
    }
  }

  applyMomentumScroll(filmstrip, velocity) {
    let currentVelocity = velocity;
    const deceleration = 0.92;

    const momentumScroll = setInterval(() => {
      if (Math.abs(currentVelocity) < 0.5) {
        clearInterval(momentumScroll);
        return;
      }

      filmstrip.scrollLeft += currentVelocity;
      currentVelocity *= deceleration;
    }, 16);
  }

  triggerRippleEffect(card, event) {
    const webglCanvas = card.querySelector('.ripple-canvas');
    if (webglCanvas) {
      webglCanvas.classList.add('is-active');
    }

    this.createCSSRipple(card, event);

    setTimeout(() => {
      if (webglCanvas) {
        webglCanvas.classList.remove('is-active');
      }
    }, 800);
  }

  createCSSRipple(card, event) {
    const rect = card.getBoundingClientRect();
    const ripple = document.createElement('div');
    ripple.className = 'ripple-effect';

    const x = event.clientX || (event.touches && event.touches[0].clientX);
    const y = event.clientY || (event.touches && event.touches[0].clientY);

    if (x && y) {
      ripple.style.left = (x - rect.left) + 'px';
      ripple.style.top = (y - rect.top) + 'px';
      ripple.style.position = 'absolute';

      card.style.position = 'relative';
      card.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 800);
    }
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new HorizontalCarousel();
  });
} else {
  new HorizontalCarousel();
}
