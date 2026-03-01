import pdfplumber
import json
import sys
from pathlib import Path

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "cours.pdf"
course = sys.argv[2] if len(sys.argv) > 2 else "GAQ"
lesson = sys.argv[3] if len(sys.argv) > 3 else "1"
title = sys.argv[4] if len(sys.argv) > 4 else "Untitled"

try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    # Nettoyage basique
    text = text.strip()
    char_count = len(text)
    
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
    
    print(f"✅ PDF extrait: {char_count} caractères")
    print(f"✅ Fichier: params.json")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)
