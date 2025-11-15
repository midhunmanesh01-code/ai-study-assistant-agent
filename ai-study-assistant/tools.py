
import json
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("memory")
MEMORY_DIR.mkdir(exist_ok=True)

NOTES_FILE = MEMORY_DIR / "notes.json"
TASKS_FILE = MEMORY_DIR / "tasks.json"


def _load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_note(title: str, content: str):
    notes = _load_json(NOTES_FILE)
    notes.append(
        {
            "title": title,
            "content": content,
            "created_at": datetime.now().isoformat(),
        }
    )
    _save_json(NOTES_FILE, notes)
    return f"Note saved: {title}"


def search_notes(query: str, top_k: int = 3):
    notes = _load_json(NOTES_FILE)
    query_lower = query.lower()
    results = []
    for n in notes:
        text = (n["title"] + " " + n["content"]).lower()
        if query_lower in text:
            results.append(n)
    return results[:top_k]


def add_task(goal: str, steps: list, deadline: str | None = None):
    tasks = _load_json(TASKS_FILE)
    tasks.append(
        {
            "goal": goal,
            "steps": steps,
            "deadline": deadline,
            "created_at": datetime.now().isoformat(),
        }
    )
    _save_json(TASKS_FILE, tasks)
    return f"Task plan saved for goal: {goal}"


def list_tasks():
    return _load_json(TASKS_FILE)
