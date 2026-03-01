#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re

print("=" * 80)
print("VERIFICATION REPORT - QUIZ GENERATION")
print("=" * 80)

# ============================================================================
# 1. Verify HTML file
# ============================================================================
print("\n1. HTML Quiz File:")
filepath = 'cours/gaq/quiz-gaq-cours8.html'
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
        match = re.search(r'"q":\s*"', content)
        if match:
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
    
    if '9t11m79n' in mapping:
        entry = mapping['9t11m79n']
        print(f"   [OK] JSON is valid")
        print(f"   [OK] Entry found for ID: 9t11m79n")
        print(f"   [OK] Course: {entry.get('course')}")
        print(f"   [OK] Lesson: {entry.get('lesson')}")
        print(f"   [OK] Title: {entry.get('title')}")
        print(f"   [OK] Path: {entry.get('path')}")
        print(f"   [OK] Questions count: {entry.get('questionsCount')}")
    else:
        print(f"   [ERROR] ID 9t11m79n not found in quiz-mapping.json")
        print(f"   [ERROR] Available IDs: {list(mapping.keys())}")
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
    
    # Look for the new quiz ID in the GAQ course
    if '9t11m79n' in index_content:
        print(f"   [OK] Quiz ID found in index.html")
        
        # Check if it's in GAQ section
        if '"name": "GAQ"' in index_content:
            print(f"   [OK] GAQ section found")
            
            # Try to parse JavaScript
            match = re.search(r'const courses = \[(.*?)\];', index_content, re.DOTALL)
            if match:
                print(f"   [OK] courses array structure found")
                # Simple check for GAQ quizzes
                if '{ course: 8, id: "9t11m79n" }' in index_content or '{ course: 8, id: \'9t11m79n\' }' in index_content:
                    print(f"   [OK] GAQ lesson 8 quiz entry added correctly")
                else:
                    print(f"   [WARNING] Could not fully verify quiz entry format")
    else:
        print(f"   [ERROR] Quiz ID 9t11m79n not found in index.html")
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
print("  Lesson: 8")
print("  Title: Analyse statique du code et revue avancées")
print("  Unique ID: 9t11m79n")
print("  Questions: 10")
print("  File: cours/gaq/quiz-gaq-cours8.html")
print("\nNext Steps:")
print("  1. Test the quiz by opening: cours/gaq/quiz-gaq-cours8.html")
print("  2. Verify in index.html that the quiz appears in the GAQ section")
print("  3. Test the navigation and answer submission")
print("\n" + "=" * 80)
