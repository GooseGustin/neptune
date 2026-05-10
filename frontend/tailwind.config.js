/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Neptune dark theme tokens
        base:    { DEFAULT: '#0f1117', 50: '#1a1d27', 100: '#22263a' },
        surface: { DEFAULT: '#1c1f2e', hover: '#252941', border: '#2e3354' },
        accent:  { DEFAULT: '#6c63ff', hover: '#7b73ff', muted: '#3d3880' },
        text:    { primary: '#e8eaf6', secondary: '#9098c0', muted: '#565e8a' },
        success: '#22c55e',
        warning: '#f59e0b',
        error:   '#ef4444',
        info:    '#38bdf8',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: { card: '12px', pill: '9999px' },
      boxShadow: {
        card:   '0 2px 16px rgba(0,0,0,0.4)',
        glow:   '0 0 20px rgba(108,99,255,0.25)',
        subtle: '0 1px 4px rgba(0,0,0,0.3)',
      },
    },
  },
  plugins: [],
}
