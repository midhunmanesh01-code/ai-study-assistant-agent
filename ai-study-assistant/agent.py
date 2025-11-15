
import json
from llm import call_llm
from tools import save_note, search_notes, add_task, list_tasks

SYSTEM_PROMPT = """You are a helpful AI Study Assistant for a B.Tech / college student.
You can:
- create study plans,
- save notes,
- search previous notes,
- list existing plans.

Think step by step. When using tools, be concise in your explanation to the user.
"""


def decide_action(user_message: str) -> dict:
    """Use the LLM to decide which action to take.

    Expected actions:
    - 'plan'
    - 'save_note'
    - 'search_notes'
    - 'list_tasks'
    - 'chat'
    """
    tool_description = """
Available actions:
1. plan(goal, deadline) - when the user wants a schedule or study plan.
2. save_note(title, content) - when the user wants to store notes or a summary.
3. search_notes(query) - when the user wants to recall something they stored.
4. list_tasks() - when the user wants to see existing plans.
5. chat() - normal conversation.

Return a JSON object like:
{"action": "plan", "arguments": {"goal": "...", "deadline": "..."}}
"""

    prompt = f"""User message: "{user_message}"

Decide the best action and arguments.
{tool_description}
Only return the JSON object, nothing else.
"""
    raw = call_llm(SYSTEM_PROMPT, prompt)

    try:
        decision = json.loads(raw)
    except Exception:
        # Fallback to simple chat if parsing fails
        decision = {"action": "chat", "arguments": {"message": user_message}}
    return decision


def run_agent(user_message: str) -> str:
    decision = decide_action(user_message)
    action = decision.get("action", "chat")
    args = decision.get("arguments", {}) or {}

    if action == "plan":
        goal = args.get("goal", user_message)
        deadline = args.get("deadline")
        plan_prompt = (
            "Create a concise, step-by-step study plan for this goal: "
            f"{goal}. Deadline (optional): {deadline}. "
            "Use bullet points."
        )
        plan_text = call_llm(SYSTEM_PROMPT, plan_prompt)
        steps = [
            s.strip("-• ").strip()
            for s in plan_text.split("\n")
            if s.strip()
        ]
        add_task(goal, steps, deadline)
        return "Here's your study plan:\n\n" + plan_text

    if action == "save_note":
        title = args.get("title", "Untitled Note")
        content = args.get("content", user_message)
        msg = save_note(title, content)
        return msg

    if action == "search_notes":
        query = args.get("query", user_message)
        results = search_notes(query)
        if not results:
            return "I couldn't find any notes matching that."
        formatted = []
        for r in results:
            formatted.append(f"**{r['title']}**\n{r['content']}\n")
        return "Here are some matching notes:\n\n" + "\n".join(formatted)

    if action == "list_tasks":
        tasks = list_tasks()
        if not tasks:
            return "You don't have any saved study plans yet."
        out_lines = []
        for t in tasks:
            out_lines.append(f"Goal: {t['goal']}")
            out_lines.append(f"Deadline: {t['deadline']}")
            out_lines.append("Steps:")
            for s in t["steps"]:
                out_lines.append(f"- {s}")
            out_lines.append("")
        return "\n".join(out_lines)

    # Default: simple chat
    reply = call_llm(SYSTEM_PROMPT, user_message)
    return reply
