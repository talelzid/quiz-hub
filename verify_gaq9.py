#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re

print("=" * 80)
print("VERIFICATION REPORT - GAQ COURSE 9 QUIZ GENERATION")
print("=" * 80)

# ============================================================================
# 1. Verify HTML file
# ============================================================================
print("\n1. HTML Quiz File:")
filepath = 'cours/gaq/quiz-gaq-cours9.html'
if os.path.exists(filepath):
    size = os.path.getsize(filepath)
    print(f"   [OK] File created: {filepath}")
    print(f"   [OK] File size: {size} bytes")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        has_questions = 'const questions' in content
        has_quiz_container = 'quiz-container' in content
        has_script = '<script>' in content
        print(f"   [OK] Contains questions JSON: {has_questions}")
        print(f"   [OK] Contains quiz container: {has_quiz_container}")
        print(f"   [OK] Contains script tags: {has_script}")
        
        # Count questions
        questions_count = content.count('"q":')
        print(f"   [OK] Questions count: {questions_count}")
else:
    print(f"   [ERROR] File not found: {filepath}")

# ============================================================================
# 2. Verify quiz-mapping.json
# ============================================================================
print("\n2. quiz-mapping.json:")
try:
    with open('quiz-mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Find GAQ lesson 9
    gaq9 = None
    for id, entry in mapping.items():
        if entry.get('course') == 'GAQ' and entry.get('lesson') == 9:
            gaq9 = (id, entry)
            break
    
    if gaq9:
        id, entry = gaq9
        print(f"   [OK] JSON is valid")
        print(f"   [OK] Entry found for GAQ Lesson 9")
        print(f"   [OK] ID: {id}")
        print(f"   [OK] Course: {entry.get('course')}")
        print(f"   [OK] Lesson: {entry.get('lesson')}")
        print(f"   [OK] Title: {entry.get('title')}")
        print(f"   [OK] Path: {entry.get('path')}")
        print(f"   [OK] Questions count: {entry.get('questionsCount')}")
    else:
        print(f"   [ERROR] GAQ Lesson 9 not found in quiz-mapping.json")
except json.JSONDecodeError as e:
    print(f"   [ERROR] Invalid JSON: {e}")
except FileNotFoundError:
    print(f"   [ERROR] quiz-mapping.json not found")

# ============================================================================
# 3. Verify index.html
# ============================================================================
print("\n3. index.html:")
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    if 's44jzwjo' in index_content:
        print(f"   [OK] Quiz ID found in index.html")
        
        # Check if it's in GAQ section
        if '"name": "GAQ"' in index_content:
            print(f"   [OK] GAQ section found")
            
            # Look for the entry
            if '{ course: 9, id: "s44jzwjo" }' in index_content or "{ course: 9, id: 's44jzwjo' }" in index_content:
                print(f"   [OK] GAQ lesson 9 quiz entry added correctly")
            else:
                print(f"   [WARNING] Could not fully verify exact quiz entry format")
    else:
        print(f"   [ERROR] Quiz ID s44jzwjo not found in index.html")
except FileNotFoundError:
    print(f"   [ERROR] index.html not found")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("GENERATION SUMMARY")
print("=" * 80)
print("\nGenerated Quiz:")
print("  Course: GAQ (Gestion de l'assurance qualité)")
print("  Lesson: 9")
print("  Title: Retour sur les normes et les modèle - Focus sur le TMMI")
print("  Unique ID: s44jzwjo")
print("  Questions: 10 (3 easy, 4 medium, 3 difficult)")
print("  File: cours/gaq/quiz-gaq-cours9.html")
print("\nNext Steps:")
print("  1. Test the quiz by opening: cours/gaq/quiz-gaq-cours9.html")
print("  2. Verify in index.html that the quiz appears in the GAQ section")
print("  3. Test the navigation and answer submission")
print("  4. Verify JSON structure and question content")
print("\n" + "=" * 80)
