
# AI Study Assistant Agent
This project is a simple **AI Study Assistant Agent** designed as a capstone-style project inspired by the 5‑Day AI Agents Intensive (Google x Kaggle). By Midhun Manesh.  
It demonstrates key agent concepts:

- Tool usage (planning, saving notes, searching notes, listing tasks)
- Lightweight memory using JSON files
- Simple agent loop that lets a model decide which tool to call
- Clean Python structure that you can extend or plug into any LLM API

---

## Project Structure

```text
ai-study-assistant/
├── main.ipynb        # Kaggle / Jupyter-friendly notebook interface
├── agent.py          # Core agent decision + orchestration logic
├── tools.py          # Tools for notes & tasks + JSON memory
├── llm.py            # LLM wrapper (plug in your own model here)
├── requirements.txt  # Python dependencies (minimal)
├── README.md
└── memory/
    ├── notes.json    # Created at runtime
    └── tasks.json    # Created at runtime
```

---

## How It Works

### 1. Agent Capabilities

The agent behaves like a study assistant for a B.Tech/college student.  
It can:

1. **Create study plans**
   - You give it a goal and (optionally) a deadline, e.g.  
     _"Help me plan for my Maths internal exam next week"_  
   - The agent calls the LLM to generate a step‑by‑step plan.
   - The plan is saved as a task in `memory/tasks.json`.

2. **Save notes**
   - You can ask it to store summaries or key points.
   - Notes are saved in `memory/notes.json`.

3. **Search notes**
   - You can ask things like:  
     _"What notes do I have about AI agents?"_
   - It does a simple text search over saved notes and returns matches.

4. **List existing plans**
   - You can ask it to show all saved study plans.

5. **Normal chat**
   - If no specific tool is needed, it just chats using the LLM.

---

## Agent Architecture

The core flow:

1. User sends a message (goal / question / instruction).
2. `agent.decide_action` uses the LLM to decide **which action to take**:
   - `"plan"`
   - `"save_note"`
   - `"search_notes"`
   - `"list_tasks"`
   - `"chat"`
3. Depending on the chosen action, the agent calls the appropriate tool function from `tools.py`.
4. The final response is returned to the user.

This matches typical AI agent patterns:
- Reasoning & decision‑making
- Tool calling
- Short‑term memory using a store (JSON files)

---

## Setup & Installation

### 1. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Currently, dependencies are minimal (`python-dotenv` is optional, only if you want env-based keys).

---

## Connecting a Real LLM

Open `llm.py`. You will see a dummy implementation:

```python
def call_llm(system_prompt: str, user_prompt: str) -> str:
    # TODO: replace with a real LLM call
    return "This is a dummy response. Plug in your LLM here."
```

Replace that with a real API call. For example, with OpenAI (pseudocode):

```python
from openai import OpenAI
client = OpenAI()

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content
```

Or with Gemini / any other provider accordingly.

> 🔐 **Never hard‑code your API key in the notebook if you upload to a public repo.**  
> Use environment variables instead (e.g. `.env` + `python-dotenv`).

---

## Running the Agent (Notebook)

Open `main.ipynb` in Jupyter / VS Code / Kaggle and run the cells in order.  
You’ll get a simple text‑based loop:

```text
You: help me plan for my DS exam on Monday
Assistant: [agent generates a study plan and saves it]
```

You can exit the loop with `exit` or `quit`.

---

## Running as a Simple CLI (Optional)

You can also run the loop from a Python script (if you create one):

```bash
python main.py
```

Where `main.py` calls `run_agent()` in a loop (see the notebook for reference).

---



This small project is done for:

- Kaggle Agent Capstone
- With Love Midhun Manesh.
