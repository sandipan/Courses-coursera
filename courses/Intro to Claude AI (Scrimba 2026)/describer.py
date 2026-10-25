
import os
import gradio as gr
import anthropic
import base64
from io import BytesIO
from PIL import Image

# Read API key from the local file
with open("api_key", "r", encoding="utf-8") as f:
    os.environ["ANTHROPIC_API_KEY"] = f.read().strip()

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")


def describe_image(image):
    if image is None:
        return "Please upload an image first."

    # Convert image to JPEG and encode it as Base64
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG")
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": (
                            "Describe this image clearly and accurately. "
                            "Identify the main subjects, objects, scene, "
                            "colors, activities, and notable details. "
                            "Do not invent details that are not visible."
                        )
                    }
                ]
            }
        ]
    )

    return "\n".join(
        block.text for block in response.content
        if block.type == "text"
    )


with gr.Blocks(title="Claude Image Describer") as demo:
    gr.Markdown("# Claude Image Describer")
    gr.Markdown("Upload an image and let Claude describe its contents.")

    with gr.Row():
        image_input = gr.Image(
            label="Upload an image",
            type="pil"
        )
        description_output = gr.Textbox(
            label="Image Description",
            lines=12,
            interactive=False
        )

    describe_button = gr.Button("Describe", variant="primary")

    describe_button.click(
        fn=describe_image,
        inputs=image_input,
        outputs=description_output
    )

if __name__ == "__main__":
    demo.launch()
