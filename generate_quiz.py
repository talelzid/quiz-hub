#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfplumber
import json
import random
import string
import os
from datetime import datetime

# ============================================================================
# STEP 1: Extract PDF Content
# ============================================================================
pdf_path = r'd:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_8_Revues avancées.pdf'
pdf = pdfplumber.open(pdf_path)
extracted_text = '\n'.join([page.extract_text() for page in pdf.pages])
pdf.close()

print(f"✅ PDF Content Extracted: {len(extracted_text)} characters")
if len(extracted_text) < 500:
    print("❌ PDF content too short (< 500 characters)")
    exit(1)

# ============================================================================
# STEP 2: Parameters
# ============================================================================
course = "GAQ"
lesson = 8
title = "Analyse statique du code et revue avancées"
questions_count = 10

print(f"✅ Parameters: course={course}, lesson={lesson}, title={title}")

# ============================================================================
# STEP 3: Generate Unique ID
# ============================================================================
def generate_unique_id(existing_ids):
    """Generate 8-character unique ID"""
    while True:
        new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        if new_id not in existing_ids:
            return new_id

# Load existing IDs from quiz-mapping.json
mapping_path = os.path.join(os.getcwd(), 'quiz-mapping.json')
with open(mapping_path, 'r', encoding='utf-8') as f:
    existing_mapping = json.load(f)
existing_ids = set(existing_mapping.keys())

unique_id = generate_unique_id(existing_ids)
print(f"✅ Generated Unique ID: {unique_id}")

# ============================================================================
# STEP 4: Prepare LLM Prompt
# ============================================================================
llm_prompt = f"""Tu es un expert en génération de questions de quiz éducatif.

CONTENU DU COURS:
---
{extracted_text}
---

TÂCHE:
Génère exactement {questions_count} questions de quiz basées sur le contenu du cours ci-dessus.

STRUCTURE REQUIS:
- Questions 1-3: FACILE (vocabulaire/concepts fondamentaux)
- Questions 4-7: MOYEN (compréhension + réflexion)
- Questions 8-10: DIFFICILE (concepts avancés, cas limites, synthèse)

CHAQUE QUESTION:
1. Doit avoir 4 options de réponse (A, B, C, D)
2. UNE SEULE bonne réponse
3. La position de la bonne réponse doit être RANDOMISÉE (index 0-3, pas toujours 1)
4. Les 3 mauvaises réponses doivent avoir explication courte (< 100 mots)
5. La bonne réponse doit avoir explication détaillée (< 200 mots) sur pourquoi c'est correct

FORMAT JSON OBLIGATOIRE (Array valide):
[
  {{
    "q": "Question texte ici ?",
    "options": [
      {{ "text": "Option 1", "explain": "Explication si faux" }},
      {{ "text": "Option 2", "explain": "Explication si faux" }},
      {{ "text": "Option 3", "explain": "Explication si faux" }},
      {{ "text": "Option 4", "explain": "Explication si faux" }}
    ],
    "correct": 0,
    "correctExplain": "Détail complet pourquoi c'est correct..."
  }}
]

RÈGLES ESSENTIELLES:
✓ Retourner EXACTEMENT {questions_count} questions
✓ JSON doit être valide (parseable)
✓ Chaque question a EXACTEMENT 4 options
✓ Index 'correct' est dans [0-3] (RANDOMISÉ, pas toujours à la position 1)
✓ Pas d'options vides
✓ Couvrir maximum de sujets du contenu du cours
✓ Pas de dupliquats de questions
✓ Texte en FRANÇAIS

RETOUR:
Retourne UNIQUEMENT l'array JSON, sans commentaires, sans markdown code blocks."""

# Save prompt for debugging
with open('prompt_for_claude.txt', 'w', encoding='utf-8') as f:
    f.write(llm_prompt)

print(f"✅ LLM Prompt prepared ({len(llm_prompt)} characters)")
print("\n" + "="*80)
print("NEXT STEP: Call Claude API to generate questions")
print("="*80)
print(f"\nPrompt saved to: prompt_for_claude.txt")
print(f"Course: {course}")
print(f"Lesson: {lesson}")
print(f"Title: {title}")
print(f"Unique ID: {unique_id}")
print(f"Questions to generate: {questions_count}")
