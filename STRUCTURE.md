# Structure du Quiz Hub

## Architecture générale

```
quiz-hub/
├── css/
│   └── style.css           ← CSS partagé pour TOUS les quiz
│
├── template/
│   └── quiz-template.html  ← GABARIT à copier pour créer nouveaux quiz
│
├── IFT-SSD/
│   ├── Cours-1/
│   │   └── quiz.html       ← Quiz du Cours 1
│   ├── Cours-2/
│   │   └── quiz.html
│   └── Cours-3/ ... Cours-N/
│
├── IFT-SQL/
│   ├── Cours-1/
│   │   └── quiz.html
│   └── ...
│
└── (tous les autres cours)
```

## Comment créer un nouveau quiz

1. **Copier le gabarit** :
   - Prendre [template/quiz-template.html](template/quiz-template.html)
   - Le copier dans le dossier du cours voulu (exemple : `IFT-SSD/Cours-3/quiz.html`)

2. **Modifier le gabarit** :
   - Changer le titre : `<title>Quiz - Cours 3</title>`
   - Changer le heading : `<h1>Quiz : [Titre du Cours] (Cours 3)</h1>`
   - Remplir le tableau `questions` avec vos questions

3. **Format des questions** :
   ```javascript
   {
       q: "Votre question ?",
       options: [
           { text: "Réponse A", explain: "Pourquoi A est faux" },
           { text: "Réponse B (correcte)", explain: "" },
           { text: "Réponse C", explain: "Pourquoi C est faux" },
           { text: "Réponse D", explain: "Pourquoi D est faux" }
       ],
       correct: 1,  // Index de la bonne réponse (0-based)
       correctExplain: "Explication complète pourquoi B est correct"
   }
   ```

## Chemins CSS

- **Depuis** : `IFT-SSD/Cours-1/quiz.html`  
- **Vers** : `../../css/style.css` ✓ (chemin relatif correct)

Le gabarit contient déjà le bon chemin : `<link rel="stylesheet" href="../../css/style.css">`

## Listes des cours à créer

- [ ] IFT-SSD (12+ cours)
- [ ] IFT-SQL (12+ cours)
- [ ] IFT-AP (12+ cours)
- [ ] ICQ (12+ cours)
- [ ] GAQ (12+ cours)
- [ ] ET (12+ cours)
- [ ] AQ-SSD (12+ cours)
- [ ] AQ-AP (12+ cours)
- [ ] Automatisation-I (12+ cours)
- [ ] Automatisation-II (12+ cours)
- [ ] RT (12+ cours)

## Caractéristiques du gabarit

✅ Questions une à une  
✅ Barre de progression colorée  
✅ Compteurs correct/incorrect en temps réel  
✅ Feedback immédiat avec explications  
✅ Récapitulation complète à la fin  
✅ Design professionnel et responsive  
✅ Scalable (2, 3, 4 réponses ou plus)  

## Notes importantes

- Le CSS est **partagé** pour tous les quiz → modifications une seule fois pour tous
- Le gabarit est **complet** → copier-coller et remplir les questions
- Les chemins relatifs fonctionnent correctement pour n'importe quelle profondeur
