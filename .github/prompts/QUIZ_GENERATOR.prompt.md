agent: QUIZ_GENERATOR
version: 1.0
type: agent-execution
language: fr
description: Générateur intelligent de quiz depuis PDF de cours - extraction contenu + génération 10 questions progressives + HTML autonome + mise à jour mapping
tags: [quiz-generation, pdf-parsing, llm-content-analysis, progressive-difficulty, html-generation, dynamic-mapping]

---

# Agent QUIZ_GENERATOR - Exécution Complète

## Objectif

Transformer un **fichier PDF de cours fourni via drag-drop** en **quiz HTML autonome et intégré** :

1. **Extraction Directe** : Parser le PDF en mémoire (sans fichiers temporaires)
2. **Génération** : 10 questions progressives (1/3 facile, 1/3 moyen, 1/3 difficile) + 4 réponses randomisées
3. **Création** : Générer fichier HTML autonome (questions intégrées en JSON)
4. **Intégration** : Mettre à jour `quiz-mapping.json` + `index.html` automatiquement

**Temps cible**: < 3 minutes | **Approche**: Scripts Python autonomes + LLM | **Avantages**: Robuste, autonome, aucune validation manuelle requise

---

## ⛔ PÉRIMÈTRE STRICT - RÈGLE ABSOLUE

### Confiance Exclusive au Contenu du PDF

Les questions générées **DOIVENT PROVENIR UNIQUEMENT** du contenu du PDF fourni.

### ✅ Autorisé
- ✓ Questions basées directement sur les sections du PDF
- ✓ Combinaisons logiques de concepts mentionnés dans le PDF
- ✓ Variations de formulation autour du contenu PDF
- ✓ Questions qui demandent l'application des concepts du PDF

### ❌ INTERDIT - Violations Graves
- ❌ Ajouter des connaissances externes au domaine
- ❌ Généraliser au-delà du périmètre du PDF
- ❌ Inférer des thèmes non explicitement abordés
- ❌ Faire appel à des notions ou exemples extérieurs non mentionnés
- ❌ Extrapoler sur des cas non couverts par le PDF

### Justification
Cette règle assure la **cohérence pédagogique** : les étudiants doivent pouvoir répondre aux questions en relisant uniquement le PDF du cours fourni. Toute extrapolation viole le contrat pédagogique et rend le quiz invalide.

---

## Input Requis

```
1. Fichier PDF (drag-drop dans le chat)
   - Chemin détecté automatiquement
   - Extension .pdf
   - Format UTF-8 ou texte
   - Taille: < 50MB
   - Contenu: ≥ 500 mots
   - Statut: Non vide (rejeter si contenu extrait < 500 caractères)

2. Paramètres Utilisateur (ligne de commande ou questions interactives)
   Requis:
   - --course MATIERE (ex: ET, GAQ, IFT-SSD, IFT-SQL, IFT-AP, ICQ, RT, AQ-AP, AQ-SSD, AUTO-1, AUTO-2)
   - --lesson N (numéro cours, ex: 1, 2, 3, 6)
   - --title "Titre du cours" (ex: "Introduction aux tests")
   
   Optionnels:
   - --questions 15 (par défaut: 10)
   - --seed VALEUR (pour reproduction; par défaut: random)

3. Configuration Intégrée (automatique)
   - quiz-mapping.json (mis à jour avec nouvel ID)
   - index.html (mise à jour tableau quizzes)
   - template/quiz-template.html (base HTML du quiz)
   - Quiz placé dans: cours/[MATIERE_MINUSCULE]/quiz-[MATIERE_MINUSCULE]-cours[N].html
```

---

## Input Format Utilisateur

### Format Appel Standard

```bash
/QUIZ_GENERATOR --course ET --lesson 1 --title "Introduction aux tests"
```

### Format Appel Minimal (questions posées)

```bash
/QUIZ_GENERATOR
# Agent demande: Quelle matière? ET
# Agent demande: Quel numéro de cours? 1
# Agent demande: Titre du cours? Introduction aux tests
```

### Help Text (si aucun paramètre ou --help)

```
📘 QUIZ_GENERATOR - Générateur de Quiz depuis PDF

USAGE:
  /QUIZ_GENERATOR [options]

OPTIONS:
  --course MATIERE     (Requis) Matière du cours
                       Valeurs: ET, GAQ, IFT-SSD, IFT-SQL, IFT-AP, ICQ, RT
                       Exemple: --course ET
  
  --lesson N          (Requis) Numéro du cours (1-10)
                      Exemple: --lesson 1
  
  --title "Texte"     (Requis) Titre descriptif du cours
                      Exemple: --title "Introduction aux tests"
  
  --questions N       (Optionnel, défaut: 10) Nombre questions
                      Valeurs: 5-20
  
  --seed VALEUR       (Optionnel) Graine pour reproduction résultats
                      Par défaut: random

EXEMPLE TEMPLATE (copier-coller):
  /QUIZ_GENERATOR --course ET --lesson 1 --title "Introduction aux tests" --questions 10

NOTES:
  • Uploader le PDF du cours via drag-drop AVANT de lancer la commande
  • Le quiz sera généré dans: cours/[matiere]/quiz-[matiere]-cours[n].html
  • Un ID unique sera généré et enregistré dans quiz-mapping.json
  • Les questions auront une difficulté progressive: facile → moyen → difficile
  • La position de la bonne réponse sera randomisée (pas toujours index 1)
```

---

## Workflow Exécution (10 étapes) - AUTONOME

**AUCUNE VALIDATION INTERMÉDIAIRE - Agent gère tout automatiquement**

### ÉTAPE 1: Valider Input PDF

- Vérifier fichier PDF trouvé dans le chat
- Vérifier extension `.pdf`
- Vérifier taille < 50MB
- Vérifier format (texte extractible, pas image pure)
- **SI ERREUR**: Rejeter avec message clair
  ```
  ❌ PDF invalide: fichier vide ou non readable
     Assurez-vous que le PDF contient du texte (pas une image scannée)
  ```

### ÉTAPE 2: Extraire Contenu Texte via Script Python (AUTONOME)

**L'agent CRÉE et EXÉCUTE extract.py SANS DEMANDER VALIDATION.**

1. **Créer script extract.py**:
   ```python
   import pdfplumber
   import json
   import sys
   from pathlib import Path
   
   pdf_path = sys.argv[1] if len(sys.argv) > 1 else "cours.pdf"
   course = sys.argv[2] if len(sys.argv) > 2 else "GAQ"
   lesson = sys.argv[3] if len(sys.argv) > 3 else "1"
   title = sys.argv[4] if len(sys.argv) > 4 else "Untitled"
   
   try:
       with pdfplumber.open(pdf_path) as pdf:
           text = ""
           for page in pdf.pages:
               text += page.extract_text() + "\n"
       
       # Nettoyage basique
       text = text.strip()
       char_count = len(text)
       
       if char_count < 500:
           print(f"❌ PDF tropcourt: {char_count} caractères (min: 500)")
           sys.exit(1)
       
       # Sauvegarder dans params.json
       output = {
           "course": course,
           "lesson": lesson,
           "title": title,
           "extracted_text": text,
           "char_count": char_count
       }
       
       with open("params.json", "w", encoding="utf-8") as f:
           json.dump(output, f, ensure_ascii=False, indent=2)
       
       print(f"✅ PDF extrait: {char_count} caractères")
       print(f"✅ Fichier: params.json")
       
   except Exception as e:
       print(f"❌ Erreur: {e}")
       sys.exit(1)
   ```

2. **Exécuter extract.py automatiquement**:
   - Appel: `python extract.py <pdf_path> <course> <lesson> <title>`
   - Aucune validation manuelle - juste exécuter
   - Si erreur: Afficher message et stop (ne pas continuer)
   - Si succès: Continuer vers ÉTAPE 3

3. **Output**: Fichier `params.json` contenant contenu PDF extrait

### ÉTAPE 3: Lire Paramètres depuis params.json

- **Ouvrir et parser** `params.json` généré par extract.py
- **Récupérer**:
  - `extracted_text` : Contenu PDF (déjà validé ≥ 500 caractères)
  - `course` : Matière (ET, GAQ, etc.)
  - `lesson` : Numéro cours
  - `title` : Titre du cours
- **Validation**: JSON valide et tous champs présents
- **SI ERREUR**: Afficher message et stop
- **Output**: Variables `course`, `lesson`, `title`, `extractedText` chargées

### ÉTAPE 4: Générer ID Unique Cryptographique

- Générer 8 caractères alphanumériques aléatoires (a-z, 0-9)
  - Format: `[a-z0-9]{8}` (ex: `a7f9e2b1`, `h8z1a3b9`)
- Vérifier PAS de collision dans `quiz-mapping.json`
  - Si collision (très rare): regénérer
- **Output**: `uniqueID` (ex: `a1b2c3d4`)

### ÉTAPE 5: Préparer Contenu pour LLM

- Structurer prompt pour Claude:
  ```
  Contenu du cours:
  [extractedText]
  
  Générez [questionsCount] questions de quiz avec la structure suivante:
  - Questions: [1-3] = facile, [4-7] = moyen, [8-10] = difficile
  - Format JSON: exact pattern ci-dessous
  - Randomiser position bonne réponse (indices 0-3)
  - Explications courtes (< 100 mots)
  
  Format requis (strictement):
  [
    {
      q: "Question texte...",
      options: [
        { text: "Option A", explain: "Explication si faux..." },
        { text: "Option B", explain: "Explication si faux..." },
        { text: "Option C", explain: "Explication si faux..." },
        { text: "Option D", explain: "Explication si faux..." }
      ],
      correct: N,  // Index de la bonne réponse (0-3, randomisé)
      correctExplain: "Détail pourquoi c'est correct..."
    }
    ... (X questions)
  ]
  ```

### ÉTAPE 6: Générer Questions via LLM/Claude

- Appeler Claude API avec prompt structuré
- Parser réponse JSON
- **Validation**:
  - ✅ Exact `questionsCount` questions
  - ✅ Chaque question a 4 options + 1 correcte
  - ✅ Index `correct` dans [0-3]
  - ✅ Chaque option a `text` + `explain`
  - ✅ `correctExplain` présent et non vide
  - ✅ Pas d'options vides
  - ✅ Difficulté progressive (vocabulaire/concepts augmenter progressivement)
- **SI ERREUR PARSING**: Regénérer 1 fois
- **Output**: `questionsArray` (array JSON 10-20 questions)

### ÉTAPE 7: Créer HTML via Script Python (AUTONOME)

**L'agent CRÉE et EXÉCUTE create_quiz.py SANS DEMANDER VALIDATION.**

1. **Créer script create_quiz.py**:
   ```python
   import json
   import sys
   from pathlib import Path
   
   # Charger paramètres et questions
   with open("params.json", "r", encoding="utf-8") as f:
       params = json.load(f)
   
   with open("questions.json", "r", encoding="utf-8") as f:
       questions = json.load(f)
   
   course = params["course"].lower()
   lesson = params["lesson"]
   title = params["title"]
   
   # Déterminer titre global selon matière
   course_titles = {
       "et": "Élaboration des tests",
       "gaq": "Gestion de l'assurance qualité",
       "ift-ssd": "Initiation à la fonction de travail d'un spécialiste",
       "ift-sql": "Initiation à la fonction de travail d'un spécialiste",
       "ift-ap": "Initiation à la fonction de travail d'un Analyste Programmeur",
       "icq": "Initiation aux concepts qualité",
       "rt": "Réalisation des tests",
       "aq-ap": "Assurance qualité - Analyste Programmeur",
       "aq-ssd": "Assurance qualité - Spécialiste",
       "auto-1": "Techniques d'automatisation I",
       "auto-2": "Techniques d'automatisation II"
   }
   
   course_title = course_titles.get(course, course.upper())
   
   # Template HTML
   html_template = f'''<!DOCTYPE html>
   <html lang="fr">
   <head>
       <meta charset="UTF-8">
       <title>Quiz - Cours {lesson}</title>
       <link rel="stylesheet" href="../../css/style.css">
   </head>
   <body>
       <div class="global-course-title">{course_title}</div>
       <h1>Quiz : {title} (Cours {lesson})</h1>
       
       <div class="progress-container">
           <div class="progress-info">
               <span id="question-counter">Question 1 / {len(questions)}</span>
               <div class="progress-stats">
                   <span class="stat-badge incorrect"><span class="stat-icon">✕</span><span id="incorrect-count">0</span></span>
                   <span class="stat-badge correct"><span class="stat-icon">✓</span><span id="correct-count">0</span></span>
               </div>
           </div>
           <div class="progress-bar-wrapper" id="progressBar"></div>
       </div>
       
       <div id="quiz-container" class="card"></div>
       <div id="feedback" class="feedback-container"></div>
       
       <div class="quiz-navigation">
           <button id="prevBtn" onclick="previousQuestion()">← Précédent</button>
           <button id="nextBtn" onclick="nextQuestion()">Suivant →</button>
       </div>
       
       <div id="result"></div>

       <script>
           const questions = {json.dumps(questions, ensure_ascii=False)};
           
           // [JavaScript du template reste inchangé]
           let currentQuestion = 0;
           let answers = new Array(questions.length).fill(null);
           let answered = new Array(questions.length).fill(false);

           function displayQuestion() {{
               const container = document.getElementById('quiz-container');
               const item = questions[currentQuestion];
               
               let html = `<div class="question">${{currentQuestion + 1}}. ${{item.q}}</div>`;
               const letters = ['A', 'B', 'C', 'D'];
               item.options.forEach((opt, i) => {{
                   let classes = '';
                   if (answers[currentQuestion] === i) {{
                       classes = 'selected ';
                       if (i === item.correct) {{
                           classes += 'correct';
                       }} else {{
                           classes += 'incorrect';
                       }}
                   }}
                   const disabledClass = answered[currentQuestion] ? 'disabled' : '';
                   html += `<div class="option ${{classes}} ${{disabledClass}}" onclick="${{answered[currentQuestion] ? '' : `handleAnswerClick(${{i}})`}}" style="${{answered[currentQuestion] ? 'cursor: not-allowed;' : ''}}"><span class="option-letter">${{letters[i]}}</span> ${{opt.text}}</div>`;
               }});
               
               container.innerHTML = html;
               
               if (answered[currentQuestion]) {{
                   showFeedback();
               }} else {{
                   document.getElementById('feedback').innerHTML = '';
                   document.getElementById('feedback').classList.remove('show');
               }}
               
               updateProgressBar();
               updateNavigationButtons();
               updateProgressInfo();
           }}

           function handleAnswerClick(index) {{
               if (answered[currentQuestion]) return;
               
               answers[currentQuestion] = index;
               answered[currentQuestion] = true;
               
               showFeedback();
               updateProgressBar();
               updateProgressInfo();
               updateNavigationButtons();
               displayQuestion();
           }}

           function showFeedback() {{
               const feedbackDiv = document.getElementById('feedback');
               const item = questions[currentQuestion];
               const isCorrect = answers[currentQuestion] === item.correct;
               const selectedOption = item.options[answers[currentQuestion]];
               
               feedbackDiv.className = 'feedback-container show ' + (isCorrect ? 'feedback-correct' : 'feedback-incorrect');
               
               let html = '';
               
               if (isCorrect) {{
                   html += `
                       <div class="feedback-header">Bonne réponse!</div>
                       <div class="feedback-explanation">${{item.correctExplain}}</div>
                   `;
               }} else {{
                   html += `
                       <div class="feedback-header">Pas tout à fait</div>
                       <div class="feedback-explanation">${{selectedOption.explain}}</div>
                       <div class="correct-answer-box">
                           <div class="correct-answer-label">✓ Bonne réponse:</div>
                           <div>${{item.options[item.correct].text}}</div>
                           <div style="margin-top: 8px; font-size: 0.9em;">${{item.correctExplain}}</div>
                       </div>
                   `;
               }}
               
               feedbackDiv.innerHTML = html;
           }}

           function updateProgressBar() {{
               const progressBar = document.getElementById('progressBar');
               progressBar.innerHTML = '';
               
               for (let i = 0; i < questions.length; i++) {{
                   const segment = document.createElement('div');
                   segment.className = 'progress-segment';
                   
                   if (!answered[i]) {{
                       segment.classList.add('unanswered');
                   }} else if (answers[i] === questions[i].correct) {{
                       segment.classList.add('correct');
                   }} else {{
                       segment.classList.add('incorrect');
                   }}
                   
                   progressBar.appendChild(segment);
               }}
           }}

           function updateNavigationButtons() {{
               const isAnswered = answered[currentQuestion];
               document.getElementById('prevBtn').disabled = currentQuestion === 0 || !isAnswered;
               document.getElementById('nextBtn').disabled = !isAnswered;
               
               if (currentQuestion === questions.length - 1) {{
                   document.getElementById('nextBtn').textContent = 'Voir Résultat';
               }} else {{
                   document.getElementById('nextBtn').textContent = 'Suivant →';
               }}
           }}

           function updateProgressInfo() {{
               document.getElementById('question-counter').textContent = `Question ${{currentQuestion + 1}} / ${{questions.length}}`;
               
               let correctCount = 0;
               let incorrectCount = 0;
               
               for (let i = 0; i < answers.length; i++) {{
                   if (answered[i]) {{
                       if (answers[i] === questions[i].correct) {{
                           correctCount++;
                       }} else {{
                           incorrectCount++;
                       }}
                   }}
               }}
               
               document.getElementById('correct-count').textContent = correctCount;
               document.getElementById('incorrect-count').textContent = incorrectCount;
           }}

           function nextQuestion() {{
               if (currentQuestion === questions.length - 1) {{
                   showFinalResults();
                   return;
               }}
               
               currentQuestion++;
               displayQuestion();
           }}

           function previousQuestion() {{
               if (currentQuestion > 0) {{
                   currentQuestion--;
                   displayQuestion();
               }}
           }}

           function showFinalResults() {{
               let score = 0;
               answers.forEach((answer, index) => {{
                   if (answer === questions[index].correct) score++;
               }});
               
               const container = document.getElementById('quiz-container');
               container.innerHTML = '<div class="question">Quiz terminé!</div>';
               
               const feedbackDiv = document.getElementById('feedback');
               feedbackDiv.className = 'feedback-container';
               feedbackDiv.innerHTML = '';
               
               let recapHtml = '<div class="recap-title">Résumé de vos réponses</div>';
               
               questions.forEach((question, index) => {{
                   const userAnswer = question.options[answers[index]];
                   const correctAnswer = question.options[question.correct];
                   const isCorrect = answers[index] === question.correct;
                   
                   recapHtml += `
                       <div class="recap-card ${{isCorrect ? 'correct' : 'incorrect'}}">
                           <div class="recap-number">Question ${{index + 1}} / ${{questions.length}}</div>
                           <div class="recap-question">${{question.q}}</div>
                           <div class="recap-answer-item user">
                               <span class="recap-label">Votre réponse:</span>
                               ${{userAnswer.text}}
                               <span class="recap-result ${{isCorrect ? 'correct' : 'incorrect'}}">
                                   ${{isCorrect ? '✓ Correct' : '✗ Incorrect'}}
                               </span>
                           </div>
                           ${{!isCorrect ? `
                               <div class="recap-answer-item correct-answer">
                                   <span class="recap-label">Bonne réponse:</span>
                                   ${{correctAnswer.text}}
                               </div>
                           ` : ''}}
                       </div>
                   `;
               }});
               
               document.getElementById('result').innerHTML = `
                   <div style="font-size: 2em; margin: 30px 0 20px;">Votre score : ${{score}} / ${{questions.length}}</div>
                   <div style="font-size: 1.1em; color: #555; margin-bottom: 30px;">Réussite : ${{Math.round(score / questions.length * 100)}}%</div>
                   <div class="recap-container">${{recapHtml}}</div>
               `;
               
               document.getElementById('prevBtn').disabled = false;
               document.getElementById('nextBtn').textContent = 'Recommencer';
               document.getElementById('nextBtn').disabled = false;
               document.getElementById('nextBtn').onclick = function() {{ location.reload(); }};
               document.getElementById('prevBtn').onclick = function() {{
                   currentQuestion = questions.length - 1;
                   displayQuestion();
               }};
           }}

           displayQuestion();
       </script>
   </body>
   </html>'''
   
   # Créer dossier cible
   course_dir = Path(f"cours/{course}")
   course_dir.mkdir(parents=True, exist_ok=True)
   
   # Écrire HTML
   output_file = course_dir / f"quiz-{course}-cours{lesson}.html"
   with open(output_file, "w", encoding="utf-8") as f:
       f.write(html_template)
   
   print(f"✅ HTML créé: {output_file}")
   ```

2. **Exécuter create_quiz.py automatiquement**:
   - Appel: `python create_quiz.py`
   - Aucune validation manuelle - juste exécuter
   - Si erreur: Afficher message et stop
   - Si succès: Continuer vers ÉTAPE 8

3. **Output**: Fichier HTML quiz dans `cours/[matiere]/quiz-[matiere]-cours[N].html`

### ÉTAPE 8: Fichier HTML Quiz Créé

- **Vérification**: Fichier HTML écrit avec succès (taille > 5KB)
- **Chemin**: `cours/[course_minuscule]/quiz-[course_minuscule]-cours[lesson].html`
- **Validation**: 
  - ✅ Fichier créé et accessible
  - ✅ Contient JSON questions valide
  - ✅ CSS relatif correct
  - ✅ JavaScript fonctionnel
- **Output**: `quizFilePath` validé

### ÉTAPE 9: Mettre à Jour quiz-mapping.json

- **Lire** `params.json` generé (contient course, lesson, title)
- **Lire** `questions.json` généré (pour compter questionsCount)
- **Générer** ID unique (8 caractères alphanumériques [a-z0-9])
- **Charger** `quiz-mapping.json`
- **Ajouter** nouvelle entrée:
  ```json
  {
    "unique_id": {
      "course": "ET",
      "lesson": 1,
      "title": "Introduction aux tests",
      "path": "cours/et/quiz-et-cours1.html",
      "createdAt": "2026-02-27T10:30:00Z",
      "questionsCount": 10
    }
  }
  ```
- **Validation**: JSON syntaxe OK, no ID collision
- **Écrire** fichier mis à jour
- **Output**: Confirmation ajout

### ÉTAPE 10: Mettre à Jour index.html

- Charger `index.html`
- Localiser section `courses` (données JavaScript):
  ```javascript
  const courses = [
    {
      name: "Gestion de l'assurance qualité",
      title: "GAQ",
      quizzes: [ ... ]
    }
  ]
  ```
- Trouver entrée `title` correspondant (`ET`, `GAQ`, etc.)
- Ajouter nouvelle entrée au tableau `quizzes`:
  ```javascript
  { course: "1", id: "a1b2c3d4" }
  ```
- Validation JavaScript: Syntaxe valide, pas de doublons ID
- Écrire fichier mis à jour
- **Output**: Confirmation mise à jour index.html

---

## Quality Gates (Verdicts)

### Validation Entrée

- ✅ **PDF** : Fichier fourni, ≥ 500 caractères texte
- ✅ **Paramètres** : `--course`, `--lesson`, `--title` tous valides
- ✅ **Matière** : Existe dans liste autorisée

### Validation Génération

- ✅ **Questions** : Exact N questions, JSON valide, 4 options chacune
- ✅ **Randomisation** : Position bonne réponse != position 1 (sauf coïncidence)
- ✅ **Difficulté** : Progressif (Q1-3 simple, Q4-7 moyen, Q8-10 difficile)
- ✅ **Périmètre** : Toutes les questions proviennent du contenu du PDF (CRITIQUE)
- ✅ **Traçabilité** : Chaque question liée à un concept explicite du PDF
- ✅ **HTML** : Valide, CSS relatif OK, taille > 5KB

### Validation Intégration

- ✅ **File System** : Fichier quiz écrit, path correct
- ✅ **quiz-mapping.json** : Entrée ajoutée, JSON valide, ID unique
- ✅ **index.html** : Nouvelle entrée ajoutée à bon endroit, JavaScript valide

### Verdict Global

**SUCCESS** si:
- ✅ PDF valide et contenu extrait
- ✅ 10 questions générées
- ✅ HTML créé + fichier écrit OK
- ✅ quiz-mapping.json + index.html mis à jour

**FAILED** si:
- ❌ PDF vide ou < 500 caractères
- ❌ Génération questions échouée (LLM timeout, format invalide)
- ❌ Écriture fichier échouée (permissions, espace disque)
- ❌ Mise à jour mapping/index échouée (JSON malformé, collision ID)

---

## Structuration Répertoires Attendue

```
quiz-hub/
├── cours/
│   ├── et/
│   │   ├── quiz-et-cours1.html  ✨ NOUVEAU
│   │   ├── quiz-et-cours2.html
│   │   └── ...
│   ├── gaq/
│   │   ├── quiz-gaq-cours6-ch1.html
│   │   └── ...
│   ├── ift-ssd/
│   │   └── ...
│   └── ... (autres matières)
├── css/
│   └── style.css
├── template/
│   └── quiz-template.html
├── index.html  ✨ MIS À JOUR
├── quiz-mapping.json  ✨ MIS À JOUR
└── quiz.html
```

---

## Mapping Matières → Dossiers

| Paramètre | Dossier | Fichier Pattern |
|-----------|---------|-----------------|
| ET | `cours/et/` | `quiz-et-coursN.html` |
| GAQ | `cours/gaq/` | `quiz-gaq-coursN.html` |
| IFT-SSD | `cours/ift-ssd/` | `quiz-ift-ssd-coursN.html` |
| IFT-SQL | `cours/ift-sql/` | `quiz-ift-sql-coursN.html` |
| IFT-AP | `cours/ift-ap/` | `quiz-ift-ap-coursN.html` |
| ICQ | `cours/icq/` | `quiz-icq-coursN.html` |
| RT | `cours/rt/` | `quiz-rt-coursN.html` |
| AQ-AP | `cours/aq-ap/` | `quiz-aq-ap-coursN.html` |
| AQ-SSD | `cours/aq-ssd/` | `quiz-aq-ssd-coursN.html` |
| AUTO-1 | `cours/auto-1/` | `quiz-auto-1-coursN.html` |
| AUTO-2 | `cours/auto-2/` | `quiz-auto-2-coursN.html` |

---

## Structuration Questions - Détail

### Répartition Difficulté

**Total 10 questions** (ou N si `--questions N`):

| Tranche | Questions | Difficulté | Critères |
|---------|-----------|-----------|---------|
| **1-3** | 3 | 🟢 **Facile** | Vocabulaire simple, concepts fondamentaux, réponse évidente avec lecture |
| **4-7** | 4 | 🟡 **Moyen** | Concepts intermédiaires, nécessite compréhension + réflexion |
| **8-10** | 3 | 🔴 **Difficile** | Concepts avancés, pièges possibles, réflexion critique, synthèse |

### Randomisation Position Bonne Réponse

- ✅ Générer indice aléatoire 0-3
- ✅ Attribuer bonne réponse à cet indice
- ✅ Les 3 autres options = fausses réponses
- ❌ **NE PAS FIXER** à position 1 (sinon utilisateurs repéreraient le pattern)

### Structure JSON Question Exact

```javascript
const questions = [
  {
    q: "Question texte ici ?",
    options: [
      { text: "Option A", explain: "Pourquoi pas: ..." },
      { text: "Option B (correcte)", explain: "" },
      { text: "Option C", explain: "Pourquoi pas: ..." },
      { text: "Option D", explain: "Pourquoi pas: ..." }
    ],
    correct: 1,  // Index (0-3) de la bonne réponse
    correctExplain: "Explication détaillée pourquoi B est correcte, contexte du cours..."
  },
  // ... 9 autres questions
];
```

---

## Prompt LLM/Claude - Template Exact

```
Tu es un expert en génération de questions de quiz éducatif.

CONTENU DU COURS:
---
[EXTRACTED_TEXT]
---

TÂCHE:
Génère exactement [QUESTIONS_COUNT] questions de quiz basées UNIQUEMENT sur le contenu du cours ci-dessus.

⚠️ CONTRAINTE CRITIQUE - PÉRIMÈTRE STRICT:
Les questions DOIVENT provenir du contenu du PDF. Strictement interdit d'utiliser:
- Des connaissances externes au PDF
- Des généralisations au-delà du périmètre du PDF
- Des thèmes ou exemples non mentionnés dans le PDF
- De l'extrapolation ou de l'inférence non basée sur le texte

Chaque question doit être TRAÇABLE DIRECTEMENT dans le contenu du PDF fourni.

STRUCTURE REQUIS:
- Questions [1-3]: FACILE (vocabulaire/concepts fondamentaux)
- Questions [4-7]: MOYEN (compréhension + réflexion)
- Questions [8-10]: DIFFICILE (concepts avancés, cas limites, synthèse)

CHAQUE QUESTION:
1. Doit avoir 4 options de réponse (A, B, C, D)
2. UNE SEULE bonne réponse
3. La position de la bonne réponse doit être RANDOMISÉE (index 0-3, pas toujours 1)
4. Les 3 mauvaises réponses doivent avoir explication courte (< 100 mots)
5. La bonne réponse doit avoir explication détaillée (< 200 mots) sur pourquoi c'est correct

FORMAT JSON OBLIGATOIRE (Array valide):
[
  {
    q: "Question texte ici ?",
    options: [
      { text: "Option 1", explain: "Explication si faux" },
      { text: "Option 2", explain: "Explication si faux" },
      { text: "Option 3", explain: "Explication si faux" },
      { text: "Option 4", explain: "Explication si faux" }
    ],
    correct: X,  // INDEX (0-3) de la BONNE réponse (RANDOMISÉ!)
    correctExplain: "Détail complet pourquoi c'est correct..."
  }
]

RÈGLES ESSENTIELLES:
✓ Retourner EXACTEMENT [QUESTIONS_COUNT] questions
✓ JSON doit être valide (parseable)
✓ Chaque question a EXACTEMENT 4 options
✓ Index 'correct' est dans [0-3] (RANDOMISÉ, pas toujours 1)
✓ Pas d'options vides
✓ Couvrir maximum de sujets du contenu du cours
✓ Pas de dupliquats de questions
✓ Texte en FRANÇAIS
✓ TOUS les sujets doivent être présents dans le PDF fourni
✓ NE PAS extrapoler ou généraliser au-delà du PDF

RETOUR:
Retourne UNIQUEMENT l'array JSON, sans commentaires, sans markdown code blocks.
```

---

## Exemple Minimal Complet

### Input
```
Fichier PDF: ET_Cours1_Introduction.pdf (2 pages)
Paramètres: --course ET --lesson 1 --title "Introduction aux tests"
```

### Étapes
1. ✅ PDF valide, ~3000 caractères extraits
2. ✅ Paramètres: course=ET, lesson=1, title="Introduction aux tests", questions=10
3. ✅ ID généré: `a7f9e2b1`
4. ✅ Claude génère 10 questions (facile→moyen→difficile, randomisé)
5. ✅ HTML créé: `cours/et/quiz-et-cours1.html`
6. ✅ quiz-mapping.json:
   ```json
   {
     "a7f9e2b1": {
       "course": "ET",
       "lesson": 1,
       "title": "Introduction aux tests",
       "path": "cours/et/quiz-et-cours1.html",
       "createdAt": "2026-02-27T10:30:00Z",
       "questionsCount": 10
     }
   }
   ```
7. ✅ index.html → ET quizzes: `[{ course: "1", id: "a7f9e2b1" }]`

### Output
```
✅ Quiz créé avec succès!
   Matière: Gestion de l'assurance qualité (ET)
   Cours: 1 - Introduction aux tests
   Questions: 10 (facile→difficile)
   Fichier: cours/et/quiz-et-cours1.html
   ID: a7f9e2b1
   
   📍 Accessible via: https://quiz-hub.app/quiz.html?id=a7f9e2b1
```

---

## Validation Critères

**Exécution Autonome - Agent ne demande AUCUNE validation intermédiaire:**

✅ **Scripts Exécution**
- [ ] extract.py créé et exécuté (sans confirmation)
- [ ] params.json généré avec contenu valide
- [ ] create_quiz.py créé et exécuté (sans confirmation)
- [ ] HTML quiz généré et écrit au bon chemin

✅ **Questions Générées**
- [ ] Exactement N questions (défaut: 10)
- [ ] JSON valide (parseable)
- [ ] Chaque question: 4 options + 1 correct (index 0-3)
- [ ] Randomisation bonne réponse active
- [ ] Difficulté progressive visible (facile→moyen→difficile)
- [ ] Tous sujets présents dans PDF (aucune extrapolation)
- [ ] questions.json généré et valide

✅ **HTML Quiz**
- [ ] Fichier créé au bon chemin: `cours/[matiere]/quiz-[matiere]-cours[N].html`
- [ ] Doctype, charset, CSS relatif OK
- [ ] JSON questions intégré et fonctionnel
- [ ] Taille > 5KB
- [ ] Ouvert en navigateur = fonctionne

✅ **Intégration Fichiers**
- [ ] quiz-mapping.json syntaxe JSON valide
- [ ] Nouvelle entrée présente + pas ID doublon
- [ ] index.html syntaxe JavaScript valide
- [ ] Nouvelle entrée quizzes présente

**Seule étape avec utilisateur**: TESTER le quiz comme étudiant

---

## ⚡ MODE AUTONOME EXPLIQUÉ

### Ce que vous attendez du USER:

**AVANT**: Uploader PDF + lancer commande
```
/QUIZ_GENERATOR --course GAQ --lesson 5 --title "L'audit de processus"
```

**PENDANT**: ✅ Nothing - Agent travaille seul
- Crée extract.py → Exécute (aucune validation)
- Crée create_quiz.py → Exécute (aucune validation)
- Met à jour mappings (aucune validation)

**APRÈS**: User TESTE le quiz
- Ouvre quiz.html?id=xxxxxx
- Répond aux questions comme un étudiant
- Valide que le contenu et difficulté sont OK

### Rapport Final que vous recevez:

```
✅ Quiz généré avec succès!
   Matière: GAQ (Gestion de l'assurance qualité)
   Cours: 5 - L'audit de processus
   Questions: 10 (3 faciles, 4 moyen, 3 difficiles)
   Fichier: cours/gaq/quiz-gaq-cours5.html
   ID: h7k2m9a1
   
   📍 Accès: https://quiz-hub.app/quiz.html?id=h7k2m9a1
   
   ✅ Fichiers créés/mis à jour:
      • extract.py (extraction PDF)
      • params.json (métadonnées + contenu)
      • create_quiz.py (génération HTML)
      • questions.json (10 questions)
      • cours/gaq/quiz-gaq-cours5.html (quiz final)
      • quiz-mapping.json (mise à jour)
      • index.html (mise à jour)
```

---

### Agent Gère Seul

Le agent n'attend PAS de validation, il gère directement les erreurs selon ce cas :

#### Erreur PDF
```
❌ PDF invalide: fichier vide ou corrompu
   Contenu extrait: XX caractères (minimum requis: 500)
   
   → Agent STOP et signale l'erreur
   → Pas de continuer avec les prochaines étapes
```

#### Erreur Paramètres
```
❌ Paramètre manquant ou invalide dans params.json
   Vérifier: course, lesson, title présents
   
   → Agent STOP et signale l'erreur
```

#### Erreur Génération LLM
```
❌ Échec génération questions (timeout, format invalide)
   
   → Agent RETRY 1 fois automatiquement (pas de demande confirmation)
   → Si persiste: STOP et signale
```

#### Erreur Intégration
```
❌ Impossible mise à jour quiz-mapping.json
   Raison: Collision ID (très rare)
   
   → Agent regénère ID unique automatiquement et réessaye
   → Si persiste après 2 tentatives: STOP et signale
```

---

## Architecture - Approche par Scripts Python Autonomes

### Exécution Autonome (Aucune Validation Manuelle Requise)

L'agent crée et exécute les scripts Python automatiquement SANS demander de validation:

```
Agent DÉTECTE PDF
    ↓
Crée extract.py + EXÉCUTE (autonome)
    ↓
Génère params.json (contenu PDF + métadonnées)
    ↓
Agent LIT params.json
    ↓
Envoie contenu à runSubagent
    ↓
Génère questions.json (10 questions)
    ↓
Crée create_quiz.py + EXÉCUTE (autonome)
    ↓
Génère HTML quiz complet
    ↓
Met à jour quiz-mapping.json + index.html
    ↓
Affiche rapport final + ID accès
```

### Scripts Python Créés

**1. extract.py** (ÉTAPE 2)
- Lit PDF directement
- Valide contenu (≥ 500 caractères)
- Écrit `params.json` avec `extracted_text`
- Exécution: Autonome, aucune confirmation

**2. create_quiz.py** (ÉTAPE 7)
- Lit `params.json` + `questions.json`
- Génère HTML complet (template + questions injected)
- Crée dossier `cours/[matiere]/`
- Écrire fichier quiz-...-cours[N].html
- Exécution: Autonome, aucune confirmation

### Avantages de cette Approche

- ✅ **Autonome** : Agent n'attend pas de validation pour scripts
- ✅ **Traçabilité** : params.json + questions.json conservés pour debug
- ✅ **Robuste** : Séparation des étapes, meilleure gestion erreurs
- ✅ **Reproductible** : On peut regénérer à partir des fichiers JSON
- ✅ **Réutilisable** : Scripts peuvent être utilisés indépendamment

### Communication avec l'Utilisateur

**Seule validation requise**: La FINALE
- Agent crée et exécute tout (scripts, génération, mise à jourmappings)
- A la fin: Affiche rapport RÉCAPITULATIF
- Utilisateur: Va simplement TESTER le quiz comme un étudiant
- Pas de validation intermédiaire ✓

---

## Notes Techniques

- **Approche** : Scripts Python autonomes (AUCUNE validation manuelle)
- **Étape 1-2** : extract.py crée + exécuté automatiquement
- **Étape 3-4** : Agent lit params.json généré
- **Étape 5-6** : Contenu envoyé à runSubagent (LLM)
- **Étape 7** : create_quiz.py crée + exécuté automatiquement
- **Étape 8-10** : quiz-mapping.json + index.html mis à jour
- **Fichiers générés** : params.json, questions.json, extract.py, create_quiz.py, quiz HTML
- **Paths** : Relatifs pour compatibilité GitHub Pages
- **Timeout** : Max 30 secondes pour runSubagent (LLM)
- **Erreurs** : Scripts gèrent leurs propres validations + logs

---

## Annexe: Commande Utilisateur Complète

**Format Appel:**
```bash
/QUIZ_GENERATOR [--course MATIERE] [--lesson N] [--title "Titre"] [--questions M] [--seed VAL]
```

**Exemples d'Appel:**
```bash
# Minimal (questions posées)
/QUIZ_GENERATOR

# Standard
/QUIZ_GENERATOR --course ET --lesson 1 --title "Introduction aux tests"

# Avec custom questions count
/QUIZ_GENERATOR --course GAQ --lesson 3 --title "Test dans le cycle de vie" --questions 15

# Avec seed reproduction
/QUIZ_GENERATOR --course ET --lesson 2 --title "Test statique" --seed 12345

# Help
/QUIZ_GENERATOR --help
```

**Résultat Attendu:**
```
✅ Quiz généré en < 2 min
✅ 10-20 questions (difficulté progressive)
✅ HTML autonome + JSON intégré
✅ Fichier quiz placé + mapping mis à jour + index.html mis à jour
✅ Accessible via ID cryptographique
✅ Compatible mobile/desktop
✅ Fonctionnalité 100% (navigation, feedback, résultats)
```

