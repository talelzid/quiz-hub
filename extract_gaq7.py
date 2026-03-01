import pdfplumber
import json
import secrets
import string

# Configuration
pdf_path = r'd:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_7_PAQ.pdf'
output_params = 'gaq7_params.json'

# Constants
course = "GAQ"
lesson = 7
title = "Le plan d'assurance qualité"
questions_count = 10

print("=" * 80)
print(f"QUIZ GENERATOR - ÉTAPE 1/2: Extraction PDF + ID Unique")
print("=" * 80)

# Extract PDF content
print(f"\n📄 Extraction du PDF: {pdf_path}")
try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    # Clean text
    text = text.strip()
    char_count = len(text)
    
    print(f"✅ Contenu extrait: {char_count} caractères")
    
    if char_count < 500:
        print(f"❌ ERREUR: Contenu trop court ({char_count} < 500 caractères)")
        exit(1)
        
except Exception as e:
    print(f"❌ ERREUR extraction PDF: {e}")
    exit(1)

# Generate unique ID (8 alphanumeric characters)
print(f"\n🔑 Génération ID unique cryptographique...")

# Load existing IDs from quiz-mapping.json
existing_ids = []
try:
    with open('quiz-mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
        existing_ids = list(mapping.keys())
except Exception as e:
    print(f"⚠️ Avertissement lecture quiz-mapping.json: {e}")

# Generate unique ID
alphabet = string.ascii_lowercase + string.digits
unique_id = None
max_attempts = 100

for _ in range(max_attempts):
    candidate = ''.join(secrets.choice(alphabet) for _ in range(8))
    if candidate not in existing_ids:
        unique_id = candidate
        break

if not unique_id:
    print(f"❌ ERREUR: Impossible de générer un ID unique après {max_attempts} tentatives")
    exit(1)

print(f"✅ ID généré: {unique_id}")

# Validate no collision
if unique_id in existing_ids:
    print(f"❌ ERREUR: Collision ID (très rare)")
    exit(1)

# Save parameters for next step
params = {
    "course": course,
    "lesson": lesson,
    "title": title,
    "questions_count": questions_count,
    "unique_id": unique_id,
    "extracted_text": text
}

with open(output_params, 'w', encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False, indent=2)

print(f"\n✅ Paramètres sauvegardés: {output_params}")
print("\n" + "=" * 80)
print("RÉSUMÉ:")
print(f"  Matière: {course}")
print(f"  Cours: {lesson}")
print(f"  Titre: {title}")
print(f"  ID: {unique_id}")
print(f"  Contenu: {char_count} caractères")
print(f"  Questions à générer: {questions_count}")
print("=" * 80)
