
"""LLM wrapper.

Right now this uses a dummy implementation so the project runs anywhere.
To make it a real AI assistant, replace `call_llm` with a real API call
(OpenAI, Gemini, etc.).
"""


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call an LLM with the given system + user prompts.

    TODO: Replace this with your real model integration.
    """
    # For now, just echo part of the user prompt so it is obvious it's a dummy.
    return (
        "Dummy LLM response.\n"
        "System prompt (truncated): "
        + system_prompt[:120]
        + "...\n\nUser said: "
        + user_prompt[:200]
        + "..."
    )
