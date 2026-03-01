#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfplumber
import json
import random
import string

# Extract PDF content
pdf_path = r'd:\Dropbox\Enseignement\Cours\GAQ\Support\GAQ_Cours_10_Gestion_Configuration.pdf'
pdf = pdfplumber.open(pdf_path)
extracted_text = '\n'.join([page.extract_text() for page in pdf.pages])
pdf.close()

print(f"✅ PDF Content Extracted: {len(extracted_text)} characters")
if len(extracted_text) < 500:
    print("❌ PDF content too short (< 500 characters)")
    exit(1)

# Generate unique ID
mapping = json.load(open('quiz-mapping.json', encoding='utf-8'))
existing_ids = set(mapping.keys())

random.seed()
for attempt in range(100):
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    if unique_id not in existing_ids:
        break

print(f"✅ Generated Unique ID: {unique_id}")

# Parameters
course = "GAQ"
lesson = 10
title = "La gestion de configuration"

print(f"\n✅ Parameters:")
print(f"   Course: {course}, Lesson: {lesson}")
print(f"   Title: {title}")
print(f"   ID: {unique_id}")

# Save for next steps
with open('gaq10_params.json', 'w', encoding='utf-8') as f:
    json.dump({
        'unique_id': unique_id,
        'course': course,
        'lesson': lesson,
        'title': title,
        'pdf_content': extracted_text
    }, f, ensure_ascii=False)

print(f"\n✅ Ready for question generation")
print(f"   PDF length: {len(extracted_text)} characters")
