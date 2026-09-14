/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        deepNavy: '#0B1220',
        darkNavy: '#101827',
        blueSlate: '#162235',
        blueSlateHover: '#1C2B42',
        brightCyan: '#22D3EE',
        purpleAccent: '#8B5CF6',
        emeraldSuccess: '#22C55E',
        amberWarning: '#F59E0B',
        coralRisk: '#F43F5E',
        softWhite: '#F8FAFC',
        blueGray: '#94A3B8',
        brand: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        navy: {
          800: '#162235',
          900: '#101827',
          950: '#0B1220',
        }
      },
    },
  },
  plugins: [],
};
