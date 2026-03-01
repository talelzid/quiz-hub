import pdfplumber
import json

pdf_path = r'd:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_5_Processus_Qualité_Audit.pdf'

print("=" * 80)
print("ÉTAPE 1-2: VALIDATION ET EXTRACTION PDF (EN MÉMOIRE)")
print("=" * 80)

try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    text = text.strip()
    char_count = len(text)
    
    print(f"\n✅ PDF trouvé et valide")
    print(f"✅ Contenu extrait: {char_count} caractères")
    
    if char_count < 500:
        print(f"❌ ERREUR: Contenu insuffisant ({char_count} < 500)")
        exit(1)
    
    # Save extracted text to JSON for next step
    data = {
        "course": "GAQ",
        "lesson": 5,
        "title": "L'audit de processus",
        "extracted_text": text,
        "char_count": char_count
    }
    
    with open('gaq5_extracted.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    
    print(f"\n📋 APERÇU CONTENU:")
    print("-" * 80)
    print(text[:600] + "...")
    print("-" * 80)
    print(f"\n✅ Paramètres:")
    print(f"   Matière: {data['course']}")
    print(f"   Cours: {data['lesson']}")
    print(f"   Titre: {data['title']}")
    print(f"   Caractères: {char_count}")
    print("\n✅ Prêt pour ÉTAPE 3: Génération des questions")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    exit(1)
