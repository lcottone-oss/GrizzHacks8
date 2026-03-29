/**
 * ============================================================
 * GAVEL ICON - Generate Minimalist Gavel SVG
 * ============================================================
 */

function createGavelIcon() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 40 40');
  svg.setAttribute('width', '40');
  svg.setAttribute('height', '40');
  svg.setAttribute('stroke-linecap', 'round');
  svg.setAttribute('stroke-linejoin', 'round');

  // Gavel head (hammer part)
  const head = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  head.setAttribute('x', '8');
  head.setAttribute('y', '4');
  head.setAttribute('width', '24');
  head.setAttribute('height', '8');
  head.setAttribute('fill', 'none');
  head.setAttribute('stroke', 'currentColor');
  head.setAttribute('stroke-width', '1.5');

  // Gavel handle
  const handle = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  handle.setAttribute('x1', '20');
  handle.setAttribute('y1', '12');
  handle.setAttribute('x2', '20');
  handle.setAttribute('y2', '36');
  handle.setAttribute('stroke', 'currentColor');
  handle.setAttribute('stroke-width', '1.5');

  // Base/strike zone line
  const base = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  base.setAttribute('x1', '6');
  base.setAttribute('y1', '38');
  base.setAttribute('x2', '34');
  base.setAttribute('y2', '38');
  handle.setAttribute('stroke', 'currentColor');
  handle.setAttribute('stroke-width', '1.5');

  svg.appendChild(head);
  svg.appendChild(handle);
  svg.appendChild(base);

  return svg;
}

export { createGavelIcon };
