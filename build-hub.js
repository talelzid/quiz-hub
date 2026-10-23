// Génère la page du hub (nom secret) avec la liste des cours chiffrée.
//
// Utilisation :
//   1. Modifier la liste des cours dans hub-data.local.json (fichier NON publié, voir .gitignore)
//   2. Lancer : node build-hub.js   (le mot de passe est demandé, ou lu dans HUB_PASSWORD)
//   3. Publier le fichier généré (hubFile dans hub-data.local.json)
const fs = require('fs');
const crypto = require('crypto');
const readline = require('readline');

const DATA_FILE = 'hub-data.local.json';
const TEMPLATE_FILE = 'hub-template.html';
const ITERATIONS = 310000;

function askPassword() {
    if (process.env.HUB_PASSWORD) return Promise.resolve(process.env.HUB_PASSWORD);
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    return new Promise(resolve => rl.question('Mot de passe du hub : ', answer => {
        rl.close();
        resolve(answer);
    }));
}

function encrypt(plaintext, password) {
    const salt = crypto.randomBytes(16);
    const iv = crypto.randomBytes(12);
    const key = crypto.pbkdf2Sync(password, salt, ITERATIONS, 32, 'sha256');
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    const data = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final(), cipher.getAuthTag()]);
    return {
        iterations: ITERATIONS,
        salt: salt.toString('base64'),
        iv: iv.toString('base64'),
        data: data.toString('base64')
    };
}

async function main() {
    const { hubFile, courses } = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    if (!hubFile || !Array.isArray(courses)) throw new Error(`${DATA_FILE} doit contenir hubFile et courses`);

    const password = await askPassword();
    if (!password) throw new Error('Mot de passe vide');

    const payload = encrypt(JSON.stringify(courses), password);
    const template = fs.readFileSync(TEMPLATE_FILE, 'utf8');
    fs.writeFileSync(hubFile, template.replace('__HUB_PAYLOAD__', JSON.stringify(payload)), 'utf8');

    const total = courses.reduce((sum, course) => sum + course.quizzes.length, 0);
    console.log(`${hubFile} généré : ${courses.length} cours, ${total} quiz.`);
}

main().catch(error => {
    console.error(error.message);
    process.exit(1);
});
