#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

# Load template
with open('d:\\Dropbox\\Enseignement\\quiz-hub\\template\\quiz-template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Load questions
with open('d:\\Dropbox\\Enseignement\\quiz-hub\\questions_gaq9.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Build questions JSON
questions_json = json.dumps(questions, ensure_ascii=False, indent=12)

# Replace title and course
html = template.replace('[Titre global du cours]', 'Gestion de l\'assurance qualité')
html = html.replace('[Titre du Cours]', 'Retour sur les normes et les modèle - Focus sur le TMMI')
html = html.replace('Cours X', 'Cours 9')

# Replace questions (find and replace the questions array)
import re
pattern = r'const questions = \[[\s\S]*?\];'
replacement = f'const questions = {questions_json};'
html = re.sub(pattern, replacement, html, count=1)

# Create directory if needed
target_dir = 'd:\\Dropbox\\Enseignement\\quiz-hub\\cours\\gaq'
os.makedirs(target_dir, exist_ok=True)

# Write file
filepath = os.path.join(target_dir, 'quiz-gaq-cours9.html')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
if os.path.exists(filepath):
    size = os.path.getsize(filepath)
    print(f"SUCCESS: File created at {filepath}")
    print(f"File size: {size} bytes")
    print(f"File exists: {os.path.exists(filepath)}")
else:
    print(f"ERROR: File was not created at {filepath}")
