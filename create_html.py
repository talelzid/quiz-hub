#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# ============================================================================
# Load generated questions
# ============================================================================
with open('questions_generated.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"✅ Loaded {len(questions)} questions")

# ============================================================================
# Parameters
# ============================================================================
course = "GAQ"
lesson = 8
title = "Analyse statique du code et revue avancées"
unique_id = "9t11m79n"

# Course mappings
course_names = {
    "ET": "Élaboration des tests",
    "GAQ": "Gestion de l'assurance qualité",
    "IFT-SSD": "Introduction aux fondamentaux des spécialistes en solutions de données",
    "IFT-SQL": "Introduction à SQL",
    "IFT-AP": "Introduction au métier d'analyseprogrammeur",
    "ICQ": "Introduction aux compétences du QA",
    "RT": "Running Tests",
    "AQ-AP": "Assurance Qualité pour analyseprogrammeurs",
    "AQ-SSD": "Assurance Qualité en solutions de données",
    "AUTO-1": "Automatisation 1",
    "AUTO-2": "Automatisation 2"
}

course_title_long = course_names.get(course, course)

# ============================================================================
# Load template
# ============================================================================
with open('template/quiz-template.html', 'r', encoding='utf-8') as f:
    template_content = f.read()

# ============================================================================
# Replace placeholders
# ============================================================================
html_content = template_content.replace(
    '[Titre global du cours]', 
    course_title_long
).replace(
    '[Titre du Cours]',
    title
).replace(
    'Cours X',
    f'Cours {lesson}'
)

# ============================================================================
# Replace questions JSON
# ============================================================================
questions_json = json.dumps(questions, ensure_ascii=False, indent=12)

# Find and replace the questions array in the script section
# Find the pattern: const questions = [ ... ];
import re
pattern = r'const questions = \[[\s\S]*?\];'

# Create replacement with our questions
replacement = f'const questions = {questions_json};'

html_content = re.sub(pattern, replacement, html_content)

# ============================================================================
# Create target directory if needed
# ============================================================================
course_lower = course.lower().replace('_', '-')
target_dir = f'cours/{course_lower}'
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"✅ Created directory: {target_dir}")

# ============================================================================
# Write HTML file
# ============================================================================
filename = f'quiz-{course_lower}-cours{lesson}.html'
filepath = os.path.join(target_dir, filename)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML Quiz Created: {filepath}")
print(f"   File size: {len(html_content)} bytes")

# ============================================================================
# Verify file was created and is readable
# ============================================================================
if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
    print(f"✅ Validation: File size OK ({os.path.getsize(filepath)} bytes)")
else:
    print(f"❌ Validation failed: File not created or too small")
    exit(1)

print("\n" + "="*80)
print("NEXT STEP: Update quiz-mapping.json and index.html")
print("="*80)
