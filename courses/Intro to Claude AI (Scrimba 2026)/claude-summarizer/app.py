import os
import anthropic
import gradio as gr

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Keep your existing summarize() function and Gradio interface.

demo.launch(server_name="0.0.0.0", server_port=7860)