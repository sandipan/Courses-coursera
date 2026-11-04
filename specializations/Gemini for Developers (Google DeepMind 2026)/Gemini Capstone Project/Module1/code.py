import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Setup & client ----------------------------------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

# Default to Gemini 3 Flash preview (override with GEMINI_MODEL="gemini-3-pro-preview" if desired)
MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")


# --- Custom functions (business logic) ---------------------------------------
def save_note(content: str, filename: str) -> str:
    """Append a note to a local text file."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n\n")
        return f"Note saved to '{filename}'."
    except Exception as e:
        return f"Error saving note: {e!r}"


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Very simple rule-based sentiment analysis."""
    text_lower = text.lower()
    pos = ["good", "great", "excellent", "positive", "happy", "love"]
    neg = ["bad", "terrible", "awful", "negative", "sad", "hate"]

    score = sum(w in text_lower for w in pos) - sum(w in text_lower for w in neg)
    label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    return {"sentiment": label, "score": score}


def generate_concise_summary(text_input: str, max_words: int) -> str:
    """Naive word-limited summary."""
    words = text_input.split()
    if max_words <= 0 or not words:
        return ""
    if len(words) <= max_words:
        return text_input
    return " ".join(words[:max_words]) + "..."


def web_research(query: str, url: str | None = None) -> Dict[str, Any]:
    """
    Use Google Search + URL Context to get fresh info and summarize it.
    This is where we integrate the google_search + url_context tools.
    """
    tools = [
        {"google_search": {}},
        {"url_context": {}},
    ]

    prompt_parts = [
        f"Use Google Search to find recent, relevant information about: {query}.",
        "Provide a short 3-bullet summary with one sentence per bullet.",
    ]
    if url:
        prompt_parts.append(f"Also read and use this URL as context if relevant: {url}")

    prompt = " ".join(prompt_parts)

    try:
        resp = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(tools=tools),
        )
        # summary_text = resp.text or ""
        summary_text = extract_text(resp)
        return {"status": "ok", "summary": summary_text}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Function schemas --------------------------------------------------------
save_note_decl = types.FunctionDeclaration(
    name="save_note",
    description="Save a short research note to a local text file.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "Text of the note."},
            "filename": {
                "type": "string",
                "description": "File name, e.g. 'research_notes.txt'.",
            },
        },
        "required": ["content", "filename"],
    },
)

analyze_sentiment_decl = types.FunctionDeclaration(
    name="analyze_sentiment",
    description="Analyze the overall sentiment of the given text.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text to analyze."}
        },
        "required": ["text"],
    },
)

generate_concise_summary_decl = types.FunctionDeclaration(
    name="generate_concise_summary",
    description="Generate a short summary of the given text.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "text_input": {"type": "string", "description": "Source text."},
            "max_words": {
                "type": "integer",
                "description": "Max words in summary.",
            },
        },
        "required": ["text_input", "max_words"],
    },
)

web_research_decl = types.FunctionDeclaration(
    name="web_research",
    description=(
        "Search the web for recent information using Google Search and "
        "optionally analyze a specific URL, then return a short summary."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Topic or question to research.",
            },
            "url": {
                "type": "string",
                "description": "Optional URL to read/analyze.",
            },
        },
        "required": ["query"],
    },
)

custom_functions_tool = types.Tool(
    function_declarations=[
        save_note_decl,
        analyze_sentiment_decl,
        generate_concise_summary_decl,
        web_research_decl,
    ]
)

# IMPORTANT: for the function-calling request, ONLY include function_declarations.
# Do NOT include google_search / url_context here, or you'll hit the 400 error.
TOOLS = [custom_functions_tool]


# --- Function-call dispatcher -------------------------------------------------
'''
def run_custom_function(fc: types.FunctionCall | Any) -> Dict[str, Any]:
    name = getattr(fc, "name", None)
    call_obj = getattr(fc, "function_call", fc)
    args = dict(getattr(call_obj, "args", {}) or {})

    try:
        if name == "save_note":
            msg = save_note(args["content"], args["filename"])
            return {"status": "ok", "message": msg}

        if name == "analyze_sentiment":
            analysis = analyze_sentiment(args["text"])
            return {"status": "ok", "analysis": analysis}

        if name == "generate_concise_summary":
            summary = generate_concise_summary(
                args["text_input"], int(args["max_words"])
            )
            return {"status": "ok", "summary": summary}

        if name == "web_research":
            return web_research(
                query=args["query"],
                url=args.get("url"),
            )

        return {"status": "error", "error": f"Unknown function '{name}'."}

    except Exception as e:
        return {"status": "error", "error": str(e)}
'''
def run_custom_function(fc: types.FunctionCall) -> Dict[str, Any]:
    name = fc.name
    args = dict(fc.args or {})

    try:
        if name == "save_note":
            msg = save_note(args["content"], args["filename"])
            return {"status": "ok", "message": msg}

        elif name == "analyze_sentiment":
            analysis = analyze_sentiment(args["text"])
            return {"status": "ok", "analysis": analysis}

        elif name == "generate_concise_summary":
            summary = generate_concise_summary(
                args["text_input"], int(args["max_words"])
            )
            return {"status": "ok", "summary": summary}

        elif name == "web_research":
            return web_research(
                query=args["query"],
                url=args.get("url"),
            )

        else:
            return {
                "status": "error",
                "error": f"Unknown function '{name}'."
            }

    except Exception as e:
        return {"status": "error", "error": str(e)}

# --- Response text helper ----------------------------------------------------
'''
def extract_text(response: types.GenerateContentResponse) -> str:
    if getattr(response, "text", None):
        return response.text
    pieces: List[str] = []
    for cand in response.candidates or []:
        if cand.content and cand.content.parts:
            for part in cand.content.parts:
                if getattr(part, "text", None):
                    pieces.append(part.text)
    return "\n".join(pieces).strip()
'''

def extract_text(response: types.GenerateContentResponse) -> str:
    """Extract only textual parts, ignoring function calls and other parts."""
    pieces: List[str] = []

    for candidate in response.candidates or []:
        content = candidate.content
        if not content or not content.parts:
            continue

        for part in content.parts:
            if part.text is not None:
                pieces.append(part.text)

    return "\n".join(pieces).strip()


# --- Two-turn function-calling per user prompt -------------------------------
def handle_user_turn(history: List[types.Content], user_prompt: str) -> str:
    # 1) User message
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_prompt)],
    )
    history.append(user_content)

    # First turn: model decides which function(s) to call
    try:
        first = client.models.generate_content(
            model=MODEL_ID,
            contents=history,
            config=types.GenerateContentConfig(
                tools=TOOLS,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True  # we manage function calling manually
                ),
            ),
        )
    except Exception as e:
        return f"Error calling the model: {e!r}"

    history.append(first.candidates[0].content)
    function_calls = first.function_calls or []

    # Model answered directly (or only used its own tools inside web_research)
    if not function_calls:
        return extract_text(first)

    # 2) Execute requested custom functions and send results back
    tool_parts: List[types.Part] = []
    for fc in function_calls:
        result = run_custom_function(fc)
        tool_parts.append(
            types.Part.from_function_response(
                name=getattr(fc, "name", None),
                response={"result": result},
            )
        )

    history.append(types.Content(role="tool", parts=tool_parts))

    # Second turn: final answer
    try:
        second = client.models.generate_content(
            model=MODEL_ID,
            contents=history,
            # Explicitly disable tool calling here too (avoids tool-config “leaking” across calls in some SDK versions)
            config=types.GenerateContentConfig(
                tools=[],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            ),
        )
    except Exception as e:
        return f"Error generating final answer: {e!r}"

    history.append(second.candidates[0].content)
    return extract_text(second)


# --- Conversation loop -------------------------------------------------------
def main() -> None:
    print("AI Research Assistant ready.")
    print("Type 'exit' to quit.\n")
    history: List[types.Content] = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        answer = handle_user_turn(history, user_input)
        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    main()

