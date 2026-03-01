import json
import re
from datetime import datetime

# Configuration
params_file = 'gaq7_params.json'
questions_file = 'questions_gaq7.json'
template_file = 'template/quiz-template.html'
mapping_file = 'quiz-mapping.json'
index_file = 'index.html'

print("=" * 80)
print(f"QUIZ GENERATOR - ÉTAPE 2/2: Création HTML + Mise à jour Mapping")
print("=" * 80)

# Load parameters
print(f"\n📥 Chargement des paramètres...")
with open(params_file, 'r', encoding='utf-8') as f:
    params = json.load(f)

course = params['course']
lesson = params['lesson']
title = params['title']
unique_id = params['unique_id']

print(f"  ✅ Matière: {course}")
print(f"  ✅ Cours: {lesson}")
print(f"  ✅ Titre: {title}")
print(f"  ✅ ID: {unique_id}")

# Load questions
print(f"\n📥 Chargement des questions...")
with open(questions_file, 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_count = len(questions)
print(f"  ✅ {questions_count} questions chargées")

# Validate questions
print(f"\n✔️ Validation des questions...")
for i, q in enumerate(questions, 1):
    assert 'q' in q, f"Question {i} manque 'q'"
    assert 'options' in q, f"Question {i} manque 'options'"
    assert len(q['options']) == 4, f"Question {i} doit avoir 4 options"
    assert 'correct' in q, f"Question {i} manque 'correct'"
    assert 0 <= q['correct'] <= 3, f"Question {i} 'correct' doit être 0-3"
    assert 'correctExplain' in q, f"Question {i} manque 'correctExplain'"

print(f"  ✅ Toutes les questions sont valides")

# Load template
print(f"\n📥 Chargement du template HTML...")
with open(template_file, 'r', encoding='utf-8') as f:
    html_template = f.read()

print(f"  ✅ Template chargé ({len(html_template)} caractères)")

# Prepare replacements
course_titles = {
    'GAQ': 'Gestion de l\'assurance qualité',
    'ET': 'Essais et Tests',
    'IFT-SSD': 'IFT - Sécurité des systèmes et des données',
    'IFT-SQL': 'IFT - SQL',
    'IFT-AP': 'IFT - Analyse et Programmation',
    'ICQ': 'Introduction à la Conception de Qualité',
    'RT': 'Revue et Test',
    'AQ-AP': 'AQ - Analyse et Programmation',
    'AQ-SSD': 'AQ - Sécurité des systèmes et des données',
    'AUTO-1': 'Automatisation 1',
    'AUTO-2': 'Automatisation 2'
}

course_title = course_titles.get(course, course)
quiz_title = f"Quiz : {title} (Cours {lesson})"

# Inject questions JSON in template
questions_json = json.dumps(questions, ensure_ascii=False, indent=2)

# Find and replace the questions array in the template
pattern = r'const questions = \[[\s\S]*?\];'
replacement = f'const questions = {questions_json};'

html_content = re.sub(pattern, replacement, html_template)

# Verify replacement worked
if 'const questions = [' not in html_content:
    print("❌ ERREUR: Impossible de trouver le pattern de questions dans le template")
    exit(1)

print(f"\n✅ Questions injectées dans le HTML")

# Determine output path
course_lower = course.lower()
output_dir = f'cours/{course_lower}'
output_filename = f'quiz-{course_lower}-cours{lesson}.html'
output_path = f'{output_dir}/{output_filename}'

# Create directory if needed
import os
os.makedirs(output_dir, exist_ok=True)

# Write HTML file
print(f"\n📝 Écriture du fichier HTML...")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(output_path)
print(f"  ✅ Fichier créé: {output_path} ({file_size} octets)")

if file_size < 5000:
    print(f"  ⚠️ AVERTISSEMENT: Fichier suspicieusement petit ({file_size} < 5000 octets)")

# Update quiz-mapping.json
print(f"\n📝 Mise à jour de {mapping_file}...")
with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Add new entry
mapping[unique_id] = {
    "course": course,
    "lesson": lesson,
    "title": title,
    "path": output_path,
    "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "questionsCount": questions_count
}

# Write updated mapping
with open(mapping_file, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"  ✅ Entrée ajoutée pour ID: {unique_id}")

# Update index.html
print(f"\n📝 Mise à jour de {index_file}...")
with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find the GAQ quizzes array and add new entry
# Pattern to find GAQ section
gaq_pattern = r'(name:\s*"Gestion de l\'assurance qualité",[\s\S]*?quizzes:\s*\[)([\s\S]*?)(\s*\])'

def add_quiz_entry(match):
    before = match.group(1)
    existing = match.group(2)
    after = match.group(3)
    
    # Create new entry
    new_entry = f'\n        {{ course: "{lesson}", id: "{unique_id}" }},'
    
    return before + existing + new_entry + after

index_content = re.sub(gaq_pattern, add_quiz_entry, index_content)

# Write updated index
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"  ✅ Entrée ajoutée au tableau GAQ quizzes")

print("\n" + "=" * 80)
print("✅ QUIZ GÉNÉRÉ AVEC SUCCÈS!")
print("=" * 80)
print(f"\n📊 RÉSUMÉ:")
print(f"  Matière: {course_title} ({course})")
print(f"  Cours: {lesson} - {title}")
print(f"  Questions: {questions_count}")
print(f"  Fichier: {output_path}")
print(f"  Taille: {file_size} octets")
print(f"  ID unique: {unique_id}")
print(f"\n🔗 Accessible via: quiz.html?id={unique_id}")
print("=" * 80)
