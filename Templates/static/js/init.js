/**
 * ============================================================
 * INITIALIZATION - Load All Design System Components
 * ============================================================
 */

function initializeDesignSystem() {
  console.log('🏛️ Initializing Civix Design System...');

  // Create gavel icon
  const gavelBtn = document.querySelector('.gavel-button');
  if (gavelBtn) {
    let iconDiv = gavelBtn.querySelector('.gavel-icon');
    
    // If gavel-icon doesn't exist, create it
    if (!iconDiv) {
      iconDiv = document.createElement('div');
      iconDiv.className = 'gavel-icon';
      gavelBtn.appendChild(iconDiv);
    }
    
    // Create SVG if it doesn't exist
    if (!iconDiv.querySelector('svg')) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 40 40');
      svg.setAttribute('width', '32');
      svg.setAttribute('height', '32');
      svg.setAttribute('stroke-linecap', 'round');
      svg.setAttribute('stroke-linejoin', 'round');

      // Gavel head
      const head = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      head.setAttribute('x', '8');
      head.setAttribute('y', '6');
      head.setAttribute('width', '24');
      head.setAttribute('height', '6');
      head.setAttribute('fill', 'none');
      head.setAttribute('stroke', 'currentColor');
      head.setAttribute('stroke-width', '1.5');

      // Gavel handle
      const handle = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      handle.setAttribute('x1', '20');
      handle.setAttribute('y1', '12');
      handle.setAttribute('x2', '20');
      handle.setAttribute('y2', '32');
      handle.setAttribute('stroke', 'currentColor');
      handle.setAttribute('stroke-width', '1.5');

      // Base line
      const base = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      base.setAttribute('x1', '6');
      base.setAttribute('y1', '34');
      base.setAttribute('x2', '34');
      base.setAttribute('y2', '34');
      base.setAttribute('stroke', 'currentColor');
      base.setAttribute('stroke-width', '1.5');

      svg.appendChild(head);
      svg.appendChild(handle);
      svg.appendChild(base);
      iconDiv.appendChild(svg);
      
      console.log('✓ Gavel icon created');
    }
  }

  // Add CSS link if not already present
  if (!document.querySelector('link[href*="design-system.css"]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/static/css/design-system.css';
    document.head.appendChild(link);
  }

  console.log('✓ Design System initialized');
}

// Run on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeDesignSystem);
} else {
  initializeDesignSystem();
}
