import os
import gradio as gr
import anthropic

#pip install gradio anthropic

with open("api_key", "r", encoding="utf-8") as f:
    os.environ["ANTHROPIC_API_KEY"] = f.read().strip()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")


def summarize(text, length):
    if not text or not text.strip():
        return "Please enter some text to summarize."

    prompt = f"""
Summarize the following text in {length}.

Preserve the main ideas, important facts, and conclusions.
Avoid repetition and do not introduce unsupported information.

TEXT:
{text}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return "\n".join(
        block.text for block in response.content
        if block.type == "text"
    )


demo = gr.Interface(
    fn=summarize,
    inputs=[
        gr.Textbox(
            label="Input Text",
            placeholder="Paste your text here...",
            lines=12
        ),
        gr.Radio(
            choices=["one short paragraph", "a few paragraphs", "a detailed summary"],
            value="a few paragraphs",
            label="Summary Length"
        )
    ],
    outputs=gr.Textbox(
        label="Claude Summary",
        lines=10
    ),
    title="Claude Text Summarizer",
    description="Summarize articles, notes, documents, and other text using Claude AI.",
    submit_btn="Summarize"
)

if __name__ == "__main__":
    demo.launch()
