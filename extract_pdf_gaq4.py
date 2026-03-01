#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_pdf_gaq4.py - PDF extraction script for GAQ Course 4
ÉTAPE 2: Extract PDF content autonomously
"""

import pdfplumber
import json
import sys
from pathlib import Path

pdf_path = r"d:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_4_BPMN_Modélisation_Processus.pdf"
course = "GAQ"
lesson = 4
title = "Modélisation de processus avec BPMN"

try:
    print(f"📖 Ouverture PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    
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
    print(f"❌ Erreur: {e}")
    sys.exit(1)
