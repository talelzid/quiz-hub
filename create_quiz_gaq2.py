#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_quiz_gaq2.py - Génère quiz GAQ cours 2 via le template officiel.
Entrées: params.json + questions_gaq2.json
"""

import json
import re
from pathlib import Path


def main():
    params = json.loads(Path("params.json").read_text(encoding="utf-8"))
    questions = json.loads(Path("questions_gaq2.json").read_text(encoding="utf-8"))
    template = Path("template/quiz-template.html").read_text(encoding="utf-8")

    course = str(params["course"]).lower()
    lesson = str(params["lesson"])
    title = str(params["title"])

    template = template.replace(
        "<div class=\"global-course-title\">[Titre global du cours]</div>",
        "<div class=\"global-course-title\">Gestion de l'assurance qualité</div>",
    )
    template = template.replace(
        "<h1>Quiz : [Titre du Cours] (Cours X)</h1>",
        f"<h1>Quiz : {title} (Cours {lesson})</h1>",
    )
    template = template.replace("<title>Quiz - Cours X</title>", f"<title>Quiz - Cours {lesson}</title>")
    template = template.replace(
        '<span id="question-counter">Question 1 / 10</span>',
        f'<span id="question-counter">Question 1 / {len(questions)}</span>',
    )

    questions_json = json.dumps(questions, ensure_ascii=False, indent=12)
    template = re.sub(
        r"const questions = \[[\s\S]*?\];",
        f"const questions = {questions_json};",
        template,
        count=1,
    )

    output = Path(f"cours/{course}/quiz-{course}-cours{lesson}.html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template, encoding="utf-8")

    print(f"✅ Quiz généré: {output.as_posix()}")
    print(f"   Questions: {len(questions)}")
    print(f"   Taille: {len(template)} caractères")


if __name__ == "__main__":
    main()
