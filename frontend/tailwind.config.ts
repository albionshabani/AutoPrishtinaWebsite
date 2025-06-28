import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#3B82F6', // A vibrant blue similar to Carvago
        'light-gray': '#F8F9FA',   // A very light, almost white-gray for the page background
        'dark-text': '#1F2937',    
        'medium-text': '#6B7280',
        'border-gray': '#E5E7EB',
      },
    },
  },
  plugins: [],
}
export default config