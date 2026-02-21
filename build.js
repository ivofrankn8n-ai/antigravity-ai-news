const fs = require('fs');

const envJs = `window.ENV = {
  SUPABASE_URL: "${process.env.SUPABASE_URL || ''}",
  SUPABASE_ANON_KEY: "${process.env.SUPABASE_ANON_KEY || ''}",
  GROQ_API_KEY: "${process.env.GROQ_API_KEY || ''}"
};
`;

fs.writeFileSync('env.js', envJs);
console.log('Generated env.js');
