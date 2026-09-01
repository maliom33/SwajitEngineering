import forms from '@tailwindcss/forms';

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          900: '#1E3A5F',
          700: '#24476f',
          500: '#3b5d82',
        },
        steel: '#64748B',
      },
      boxShadow: {
        glass: '0 24px 80px rgba(30, 58, 95, 0.08)',
      },
    },
  },
  plugins: [forms],
};
