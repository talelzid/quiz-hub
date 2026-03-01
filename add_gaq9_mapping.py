#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
import string

# Re-generate the unique ID (same deterministic logic)
mapping = json.load(open('quiz-mapping.json', encoding='utf-8'))
existing_ids = set(mapping.keys())

# Generate new unique ID
random.seed()
for attempt in range(100):
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    if unique_id not in existing_ids:
        print(f"Generated unique ID: {unique_id}")
        break

course = "GAQ"
lesson = 9
title = "Retour sur les normes et les modèle - Focus sur le TMMI"
filepath = "cours/gaq/quiz-gaq-cours9.html"

# Add new entry
mapping[unique_id] = {
    "course": course,
    "lesson": lesson,
    "title": title,
    "path": filepath,
    "createdAt": "2026-03-01T00:00:00Z",
    "questionsCount": 10
}

# Write updated mapping
with open('quiz-mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"✅ Updated quiz-mapping.json")
print(f"   ID: {unique_id}")
print(f"   Entry: {json.dumps(mapping[unique_id], ensure_ascii=False, indent=2)}")

# Save for next steps
with open('.gaq9_id', 'w') as f:
    f.write(unique_id)
