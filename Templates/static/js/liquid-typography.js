/**
 * ============================================================
 * LIQUID TYPOGRAPHY - Hover Reactive Text Effects
 * ============================================================
 */

class LiquidTypography {
  constructor() {
    this.liquidTitles = document.querySelectorAll('.liquid-title');
    this.reactiveTexts = document.querySelectorAll('.reactive-text');
    this.init();
  }

  init() {
    // Liquid titles - spread apart on hover
    this.liquidTitles.forEach((title) => {
      title.addEventListener('mouseenter', () => {
        title.style.letterSpacing = '8px';
        title.style.fontWeight = '800';
      });

      title.addEventListener('mouseleave', () => {
        title.style.letterSpacing = '0px';
        title.style.fontWeight = 'inherit';
      });
    });

    // Reactive text - underline reveal + weight shift
    this.reactiveTexts.forEach((text) => {
      const originalFontWeight = window.getComputedStyle(text).fontWeight;

      text.addEventListener('mouseenter', () => {
        text.style.fontWeight = '700';
        text.style.letterSpacing = '2px';
      });

      text.addEventListener('mouseleave', () => {
        text.style.fontWeight = originalFontWeight;
        text.style.letterSpacing = 'normal';
      });
    });

    // Letter-by-letter reveal animation on scroll
    this.observeTextElements();
  }

  observeTextElements() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          this.animateTextReveal(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    // Observe all headings
    document.querySelectorAll('.legal-heading, .liquid-title').forEach((el) => {
      observer.observe(el);
    });
  }

  animateTextReveal(element) {
    const text = element.textContent;
    if (!text) return;

    // Create span elements for each character
    const chars = text.split('').map((char) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.display = 'inline-block';
      span.style.opacity = '0';
      span.style.transition = 'opacity 0.6s ease-out';
      return span;
    });

    element.textContent = '';
    chars.forEach((char) => element.appendChild(char));

    // Stagger animation
    chars.forEach((char, index) => {
      setTimeout(() => {
        char.style.opacity = '1';
      }, index * 30);
    });
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new LiquidTypography();
  });
} else {
  new LiquidTypography();
}
