# Quiz Hub - Plateforme Centralisée de Quiz

Une plateforme de quiz modulaire et réutilisable pour tous vos cours. Chaque cours est découpé en séances de 4h avec son propre quiz.

## 📋 Structure du Projet

Voir [STRUCTURE.md](STRUCTURE.md) pour la documentation complète de l'architecture.

### Vue rapide
```
quiz-hub/
├── css/                    ← CSS partagé pour TOUS les quiz
├── template/               ← Gabarit pour créer nouveaux quiz
├── IFT-SSD/               ← Exemple de cours complet
│   ├── Cours-1/
│   │   └── quiz.html
│   └── Cours-2/
│       └── quiz.html
└── (10 autres cours + structures)
```

## 🚀 Quick Start

### Créer un nouveau quiz
1. Copier `template/quiz-template.html`
2. Placer dans `NomDuCours/Cours-X/quiz.html`
3. Remplir les questions dans le tableau `questions`
4. C'est tout !

### Exemple : IFT-SSD/Cours-1
Le fichier [IFT-SSD/Cours-1/quiz.html](IFT-SSD/Cours-1/quiz.html) est complet et prêt à fonctionner.

## ✨ Fonctionnalités

- ✅ Questions présentées une à une
- ✅ Barre de progression colorée (gris/vert/rouge)
- ✅ Compteurs de réponses correctes/incorrectes en temps réel
- ✅ Feedback immédiat avec explications détaillées
- ✅ Récapitulation complète à la fin avec toutes les réponses
- ✅ Design professionnel et sobre
- ✅ Navigation avant/arrière
- ✅ CSS partagé et centralisé
- ✅ Scalable : fonctionne avec 2, 3, 4+ réponses

## 📚 Cours à créer

- IFT-SSD
- IFT-SQL
- IFT-AP
- ICQ
- GAQ
- ET
- AQ-SSD
- AQ-AP
- Automatisation-I
- Automatisation-II
- RT

## 📝 Format des Questions

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

## 🔗 Chemins CSS

Le chemin CSS est configuré automatiquement dans le gabarit :
```html
<link rel="stylesheet" href="../../css/style.css">
```

Cela fonctionne pour toute structure : `Cours-1/`, `Cours-2/`, etc.

## 📖 Documentation

- [STRUCTURE.md](STRUCTURE.md) - Architecture détaillée et instructions