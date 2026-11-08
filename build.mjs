// Builds build/index.html (unencrypted) from src/app.html.
// The deploy workflow then encrypts it with StatiCrypt into dist/.
// The games themselves are not in this repo: the app loads them from the private data repo.
import { readFileSync, writeFileSync, mkdirSync, cpSync } from 'node:fs';

const version = new Date().toISOString();
const html = readFileSync('src/app.html', 'utf8').replace('/*VERSION*/', version);
mkdirSync('build', { recursive: true });
writeFileSync('build/index.html', html);
cpSync('public', 'build', { recursive: true });
writeFileSync('build/version.json', JSON.stringify({ version }));
console.log('build/index.html');
