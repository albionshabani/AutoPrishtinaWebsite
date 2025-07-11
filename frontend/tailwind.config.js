// FILE: frontend/tailwind.config.js

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {

      keyframes: {
        // This is the animation from your example
        fill: {
          '0%': { transform: 'scale(0)', opacity: '0' },
          '50%': { transform: 'scale(1.2)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      animation: {
        // This creates a utility class `animate-fill` that we can use
        fill: 'fill 0.4s ease-in-out',
      },

      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },

      backgroundImage: {
        'blue-diagonal': 'linear-gradient(45deg, #0E3467, #1C68CD)',
      },
    
      // --- THIS IS THE NEW, CENTRALIZED COLOR PALETTE ---
      colors: {
        'background': '#f5f5f5',     // The main, slightly-off-white background
        'surface': '#ffffff',      // The background for cards, headers, footers
        'primary': '#0078d4',      // The main brand blue for buttons and links
        
        'text-primary': '#1c1c1c',   // For headings and important text
        'text-secondary': '#667085', // For descriptions and less-important text
        'text-on-primary': '#ffffff',// Text that appears on a primary-colored background
        
        'border-primary': '#d0d5dd',  // Main border color
        'border-secondary': '#e5e7eb',// Lighter border color for subtle lines
        
        'subtle': '#f9fafb',       // A very light gray for hover states
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true
  }
}