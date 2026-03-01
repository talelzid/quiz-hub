#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_quiz.py - Génère un quiz HTML à partir de params.json + questions.json
Modèle: template/quiz-template.html
"""

import json
import re
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_questions(questions):
    normalized = []
    for item in questions:
        options = []
        for option in item.get("options", []):
            if isinstance(option, dict):
                options.append(
                    {
                        "text": str(option.get("text", "")),
                        "explain": str(option.get("explain", "")),
                    }
                )
            else:
                options.append({"text": str(option), "explain": ""})

        normalized.append(
            {
                "q": str(item.get("q", "")),
                "options": options,
                "correct": int(item.get("correct", 0)),
                "correctExplain": str(item.get("correctExplain", "")),
            }
        )

    return normalized


def main():
    params_path = Path("params.json")
    questions_path = Path("questions.json")
    template_path = Path("template/quiz-template.html")

    params = load_json(params_path)
    questions = normalize_questions(load_json(questions_path))

    course = str(params["course"]).lower()
    lesson = str(params["lesson"])
    title = str(params["title"])

    course_titles = {
        "et": "Élaboration des tests",
        "gaq": "Gestion de l'assurance qualité",
        "ift-ssd": "Initiation à la fonction de travail d'un spécialiste",
        "ift-sql": "Initiation à la fonction de travail d'un spécialiste",
        "ift-ap": "Initiation à la fonction de travail d'un Analyste Programmeur",
        "icq": "Initiation aux concepts qualité",
        "rt": "Réalisation des tests",
        "aq-ap": "Assurance qualité - Analyste Programmeur",
        "aq-ssd": "Assurance qualité - Spécialiste",
        "auto-1": "Techniques d'automatisation I",
        "auto-2": "Techniques d'automatisation II",
    }
    global_title = course_titles.get(course, course.upper())

    html = template_path.read_text(encoding="utf-8")

    html = html.replace(
        "<div class=\"global-course-title\">[Titre global du cours]</div>",
        f"<div class=\"global-course-title\">{global_title}</div>",
    )
    html = html.replace(
        "<h1>Quiz : [Titre du Cours] (Cours X)</h1>",
        f"<h1>Quiz : {title} (Cours {lesson})</h1>",
    )
    html = html.replace("<title>Quiz - Cours X</title>", f"<title>Quiz - Cours {lesson}</title>")
    html = html.replace(
        '<span id="question-counter">Question 1 / 10</span>',
        f'<span id="question-counter">Question 1 / {len(questions)}</span>',
    )

    questions_json = json.dumps(questions, ensure_ascii=False, indent=12)
    html = re.sub(
        r"const questions = \[[\s\S]*?\];",
        f"const questions = {questions_json};",
        html,
        count=1,
    )

    output_dir = Path("cours") / course
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"quiz-{course}-cours{lesson}.html"
    output_file.write_text(html, encoding="utf-8")

    print(f"✅ HTML quiz généré: {output_file.as_posix()}")
    print(f"   Questions: {len(questions)}")
    print(f"   Taille: {len(html)} octets")


if __name__ == "__main__":
    main()
