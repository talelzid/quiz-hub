#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re

# Load parameters
with open('gaq10_params.json', 'r', encoding='utf-8') as f:
    params = json.load(f)

# Load questions
with open('questions_gaq10.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

unique_id = params['unique_id']
course = params['course']
lesson = params['lesson']
title = params['title']

print(f"✅ Loaded {len(questions)} questions")
print(f"   ID: {unique_id}")
print(f"   Course: {course}, Lesson: {lesson}")
print(f"   Title: {title}")

# Load template
with open('template/quiz-template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace placeholders
html = template.replace('[Titre global du cours]', 'Gestion de l\'assurance qualité')
html = html.replace('[Titre du Cours]', title)
html = html.replace('Cours X', f'Cours {lesson}')

# Replace questions JSON
questions_json = json.dumps(questions, ensure_ascii=False, indent=12)
pattern = r'const questions = \[[\s\S]*?\];'
replacement = f'const questions = {questions_json};'
html = re.sub(pattern, replacement, html, count=1)

# Create directory and write file
target_dir = 'cours/gaq'
os.makedirs(target_dir, exist_ok=True)
filepath = f'{target_dir}/quiz-gaq-cours{lesson}.html'

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

file_size = os.path.getsize(filepath)
print(f"\n✅ HTML Quiz Created: {filepath}")
print(f"   File size: {file_size} bytes")

# Update quiz-mapping.json
with open('quiz-mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

mapping[unique_id] = {
    "course": course,
    "lesson": lesson,
    "title": title,
    "path": filepath.replace('\\', '/'),
    "createdAt": "2026-03-01T00:00:00Z",
    "questionsCount": len(questions)
}

with open('quiz-mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"\n✅ Updated quiz-mapping.json")
print(f"   Added entry for ID: {unique_id}")

print(f"\n✅ Generation complete!")
