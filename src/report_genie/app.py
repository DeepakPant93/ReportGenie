import gradio as gr
import os
from report_genie.crew import ExpresslyServer


def call(prompt, target_audience, format, tone, active_tab):
    """
    Calls the Expressly Server API to generate content based on the given inputs.

    Args:
    prompt (str): The text prompt for the chat.
    target_audience (str): The target audience for the response.
    format (str): The format of the response, e.g., text, markdown.
    tone (str): The tone of the response, e.g., formal, informal.
    active_tab (str): The active tab on the UI, either "target_audience" or "format_tone".

    Returns:
    str: The generated text response.

    Raises:
    ValueError: If prompt is empty, or if the active_tab value is invalid.
    """

    # Validating and constructing the inputs
    if prompt is None or prompt == "":
        raise ValueError("Prompt is required")

    if active_tab == "target_audience":
        format = ""
        tone = ""
    elif active_tab == "format_tone":
        target_audience = ""
    else:
        raise ValueError("Invalid active_tab value")

    inputs = {
        "prompt": prompt,
        "target_audience": target_audience,
        "format": format,
        "tone": tone,
    }

    outputs = ExpresslyServer().crew().kickoff(inputs=inputs)

    if outputs is None:
        result = "Please check the inputs and try again. If the issue persists, contact support."
    else:
        result = outputs.raw

    return result


with gr.Blocks() as app:
    gr.Markdown("# Expressly - Text Transformation App")

    with gr.Row():
        # Left Column for Inputs
        with gr.Column(scale=1):
            prompt = gr.Textbox(label="Message Expressly", max_length=1024, lines=3)

            # Create a state variable to store active tab
            active_tab = gr.State("target_audience")

            with gr.Tab("Target Audience", id="tab_audience") as tab1:
                target_audience = gr.Dropdown(
                    [
                        "LinkedIn Post",
                        "WhatsApp Message",
                        "Tweet",
                        "News Article",
                        "Technical Blog",
                        "Formal Email",
                        "Instagram Post",
                        "Website Content",
                        "Marketing Email",
                        "Job Application",
                        "Customer Support Response",
                    ],
                    label="Target Audience",
                    info="Pick a Target Audience to specify the purpose or platform.",
                )
                # Update state when this tab is selected
                tab1.select(lambda: "target_audience", None, active_tab)

            with gr.Tab("Format & Tone", id="tab_format") as tab2:
                format = gr.Dropdown(
                    [
                        "Post",
                        "Chat",
                        "Tweet",
                        "Email",
                        "Blog",
                        "Article",
                        "Report",
                        "Product Description",
                    ],
                    label="Format",
                    info="Choose a Format to define the type of content.",
                )
                tone = gr.Dropdown(
                    [
                        "Professional",
                        "Casual",
                        "Straightforward",
                        "Confident",
                        "Friendly",
                        "Neutral",
                        "Storytelling",
                        "Inspirational",
                    ],
                    label="Tone",
                    info="Select a Tone to set the communication style.",
                )
                # Update state when this tab is selected
                tab2.select(lambda: "format_tone", None, active_tab)

            btn_submit = gr.Button("Submit")

        # Right Column for Output
        with gr.Column(scale=1):
            results = gr.Markdown(label="Result")

    btn_submit.click(
        fn=call,
        inputs=[prompt, target_audience, format, tone, active_tab],
        outputs=[results],
    )


def launch():
    print("Launching Gradio app at 10000...")
    app.queue(max_size=10).launch(server_port=10000)


if __name__ == "__main__":
    launch()
