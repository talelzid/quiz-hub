import pdfplumber
import json
import sys
from pathlib import Path

pdf_path = r"d:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_3_Exigences_Qualité_Métriques.pdf"
course = "GAQ"
lesson = 3
title = "Éxigences qualité et définition de métriques - IEEE 1061"

try:
    print(f"📖 Ouverture PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    # Nettoyage basique
    text = text.strip()
    char_count = len(text)
    
    print(f"✅ Extraction complète: {char_count} caractères")
    
    if char_count < 500:
        print(f"❌ PDF trop court: {char_count} caractères (min: 500)")
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
    
    print(f"✅ Fichier params.json généré")
    print(f"   Contenu: {char_count} caractères")
    print(f"   Statut: Prêt pour ÉTAPE 3")
    
except Exception as e:
    print(f"❌ Erreur extraction: {e}")
    sys.exit(1)
