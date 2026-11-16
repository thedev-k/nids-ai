/**
 * NIDS Intelligence Dashboard â€” Bespoke Chart Engine
 * Plotly.js Visualizations + GSAP Entrance Animations
 *
 * Implements:
 * - displayModeBar: false (clean, bespoke chart styling with no default toolbar)
 * - Deep custom Plotly theming for Flight Tracker Dark Material
 * - Custom center cutout & annotations for Class Imbalance Donut
 * - Wide margins and rounded breathing room for Attack Vector Bar Chart
 * - Dynamic update of HorizonX telemetry progress indicators
 */

/* â”€â”€ Plotly Bespoke Config: Toolbar Completely Hidden â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const PLOTLY_CONFIG = {
  responsive: true,
  displayModeBar: false, // Strict requirement: remove default hover toolbar
  displaylogo: false
};

/* â”€â”€ Dark Base Theme Layout â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const DARK_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font: {
    family: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    color:  '#8c96a8',
    size:   11
  }
};

const GRID_COLOR = 'rgba(255, 255, 255, 0.05)';
const ZERO_COLOR = 'rgba(255, 255, 255, 0.09)';

/* â”€â”€ Utility Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
async function fetchJSON(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status} â€” ${url}`);
    return await res.json();
  } catch (err) {
    console.error('[NIDS API Error]', err.message);
    return null;
  }
}

function fmt(n) {
  if (n === null || n === undefined) return 'â€”';
  return Number(n).toLocaleString();
}

function el(id) {
  return document.getElementById(id);
}

/* â”€â”€ Main Dashboard Initialization â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
async function initDashboard() {

  /* 1. GSAP Entrance Animation (with reduced-motion guard) */
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (window.gsap && !prefersReducedMotion) {
    gsap.fromTo(
      '.animate-card',
      { opacity: 0, y: 16 },
      {
        opacity: 1,
        y: 0,
        duration: 0.5,
        stagger: 0.06,
        ease: 'power2.out',
        clearProps: 'all' // Prevents inline styles from ever trapping the DOM
      }
    );
  }

  /* 2. Health Check & Live Beacon */
