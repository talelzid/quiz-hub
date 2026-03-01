#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('_temp/gaq9_ready.json', 'r') as f:
    data = json.load(f)

unique_id = data['unique_id']
course = data['course']
lesson = data['lesson']
title = data['title']
filepath = data['filepath']

# Load existing mapping
with open('quiz-mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Check for collision
if unique_id in mapping:
    print(f"❌ ID collision: {unique_id} already exists")
    exit(1)

# Add new entry
mapping[unique_id] = {
    "course": course,
    "lesson": lesson,
    "title": title,
    "path": filepath.replace('\\', '/'),
    "createdAt": "2026-03-01T00:00:00Z",
    "questionsCount": 10
}

# Write updated mapping
with open('quiz-mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"✅ Updated quiz-mapping.json")
print(f"   ID: {unique_id}")
print(f"   Course: {course}, Lesson: {lesson}")
print(f"   Entry: {json.dumps(mapping[unique_id], ensure_ascii=False, indent=2)}")
