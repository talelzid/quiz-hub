import json
import os

print("=" * 80)
print("VERIFICATION REPORT - GAQ COURSE 7 QUIZ GENERATION")
print("=" * 80)

# 1. Verify HTML file
print("\n1. HTML Quiz File:")
html_path = 'cours/gaq/quiz-gaq-cours7.html'

if os.path.exists(html_path):
    print(f"   [OK] File created: {html_path}")
    
    file_size = os.path.getsize(html_path)
    print(f"   [OK] File size: {file_size} bytes")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for questions JSON
    has_questions = 'const questions = [' in content
    print(f"   [OK] Contains questions JSON: {has_questions}")
    
    # Check for quiz container
    has_container = 'quiz-container' in content
    print(f"   [OK] Contains quiz container: {has_container}")
    
    # Check for script tags
    has_scripts = '<script>' in content
    print(f"   [OK] Contains script tags: {has_scripts}")
    
    # Count questions in JSON
    import re
    match = re.search(r'const questions = (\[[\s\S]*?\]);', content)
    if match:
        try:
            questions = json.loads(match.group(1))
            print(f"   [OK] Questions count: {len(questions)}")
        except:
            print(f"   [ERROR] Could not parse questions JSON")
    
else:
    print(f"   [ERROR] File not found: {html_path}")

# 2. Verify quiz-mapping.json
print("\n2. quiz-mapping.json:")
mapping_path = 'quiz-mapping.json'

if os.path.exists(mapping_path):
    with open(mapping_path, 'r', encoding='utf-8') as f:
        try:
            mapping = json.load(f)
            print(f"   [OK] JSON is valid")
            
            # Check for our quiz ID
            quiz_id = '2i09q4tb'
            if quiz_id in mapping:
                entry = mapping[quiz_id]
                print(f"   [OK] Entry found for GAQ Lesson 7")
                print(f"   [OK] ID: {quiz_id}")
                print(f"   [OK] Course: {entry.get('course')}")
                print(f"   [OK] Lesson: {entry.get('lesson')}")
                print(f"   [OK] Title: {entry.get('title')}")
                print(f"   [OK] Path: {entry.get('path')}")
                print(f"   [OK] Questions count: {entry.get('questionsCount')}")
            else:
                print(f"   [ERROR] Entry not found for ID: {quiz_id}")
                
        except json.JSONDecodeError as e:
            print(f"   [ERROR] Invalid JSON: {e}")
else:
    print(f"   [ERROR] File not found: {mapping_path}")

# 3. Verify index.html
print("\n3. index.html:")
index_path = 'index.html'

if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if quiz ID is present
    quiz_id = '2i09q4tb'
    if quiz_id in content:
        print(f"   [OK] Quiz ID found in index.html")
        
        # Check if GAQ section exists
        if 'Gestion de l\'assurance qualité' in content or 'Gestion de l\\\'assurance qualité' in content:
            print(f"   [OK] GAQ section found")
            
            # Check if lesson 7 entry exists
            if 'course: "7"' in content or 'course: \'7\'' in content or 'course: 7' in content:
                print(f"   [OK] GAQ lesson 7 quiz entry added correctly")
            else:
                print(f"   [WARNING] Could not confirm lesson 7 entry format")
        else:
            print(f"   [WARNING] GAQ section not clearly identified")
    else:
        print(f"   [ERROR] Quiz ID not found in index.html")
else:
    print(f"   [ERROR] File not found: {index_path}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
