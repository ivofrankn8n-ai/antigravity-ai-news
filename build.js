const fs = require('fs');

const envJs = `window.ENV = {
  SUPABASE_URL: "${process.env.SUPABASE_URL || ''}",
  SUPABASE_ANON_KEY: "${process.env.SUPABASE_ANON_KEY || ''}",
  GROQ_API_KEY: "${process.env.GROQ_API_KEY || ''}"
};
`;

// Also update dashboard.html placeholders with actual values
let dashboard = fs.readFileSync('dashboard.html', 'utf8');
dashboard = dashboard.replace(
  /SUPABASE_URL_PLACEHOLDER/g, 
  process.env.SUPABASE_URL || ''
);
dashboard = dashboard.replace(
  /SUPABASE_KEY_PLACEHOLDER/g, 
  process.env.SUPABASE_ANON_KEY || ''
);
dashboard = dashboard.replace(
  /GROQ_KEY_PLACEHOLDER/g, 
  process.env.GROQ_API_KEY || ''
);

fs.writeFileSync('dashboard.html', dashboard);
fs.writeFileSync('env.js', envJs);

console.log('Build complete - env.js generated and dashboard.html updated');
