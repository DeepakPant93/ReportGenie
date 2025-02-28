import gradio as gr
import os
from report_genie.crew import ReportGenieServer
from report_genie.utils.utils import load_json_data


# Load the JSON files
CITIES_JSON_FILE = "cities.json"
INDUSTRIES_JSON_FILE = "industries.json"
KNOWLEDGE_SOURCE_PATH = "knowledge"

cities = load_json_data(CITIES_JSON_FILE, KNOWLEDGE_SOURCE_PATH)
industries = load_json_data(INDUSTRIES_JSON_FILE, KNOWLEDGE_SOURCE_PATH)

def generate_report(city, industry):
 
    inputs = {
        "city_name": city,
        "industry_name": industry,
    }

    try:
        output = ReportGenieServer().crew().kickoff(inputs=inputs)
    except Exception:
        output = None

    if output is None:
        result = "Please check the inputs and try again. If the issue persists, contact support."
    else:
        result = output.raw

    return result


## Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# 📄 Report Genie - An AI-powered automatic report generator")
    gr.Markdown("Report Genie is an AI-driven report generation tool that automates the process of creating detailed and structured reports. Leveraging the power of **CrewAI** for task delegation and **Gradio** for an interactive user interface, this application streamlines report generation with minimal user input.")
    
    with gr.Row():
        city_input = gr.Dropdown(choices=cities.get("cities"), label="Select City")
        industry_input = gr.Dropdown(choices=industries.get("industries"), label="Select Industry")
        submit_button = gr.Button("Generate Report")

    gr.Markdown("---")
    gr.Markdown("---")
    gr.Markdown("---")

    report_output = gr.Markdown(value="", label="Report", visible=False)
    
    def on_submit(city, industry):
        return gr.update(value=generate_report(city, industry), visible=True)
    
    submit_button.click(on_submit, inputs=[city_input, industry_input], outputs=report_output)

def launch():
    """
    Launch the Expressly web app.
    This function starts the Expressly web app in a threaded mode, allowing it
    to process multiple requests concurrently. The app is configured to
    accept up to 10 requests in its queue at any given time.
    The app is launched with strict CORS checks disabled, which allows it
    to be accessed from any origin.
    To launch the app, call this function with no arguments.
    Example:
        launch()
    """
    app.queue(max_size=10).launch(strict_cors=False)

if __name__ == "__main__":
    launch()
