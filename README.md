---
title: Report Genie
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
license: mit
short_description: Report Genie - An AI-powered automatic report generator
---

# Report Genie - An AI-powered automatic report generator

**An AI-powered automatic report generator using CrewAI and Gradio**

## Overview
Report Genie is an AI-driven report generation tool that automates the process of creating detailed and structured reports. Leveraging the power of **CrewAI** for task delegation and **Gradio** for an interactive user interface, this application streamlines report generation with minimal user input.

## Features
- **AI-powered automation**: Uses advanced AI agents to generate reports.
- **Interactive UI**: Built with Gradio for an intuitive and user-friendly interface.
- **Customizable reports**: Supports multiple report formats and structures.
- **Efficient task delegation**: CrewAI intelligently assigns subtasks to optimize the workflow.
- **Seamless integration**: Can be integrated with external data sources for enhanced report accuracy.
- **Company data retrieval**: Uses Neo4J to fetch company data from the database.

## Tech Stack
- **Python**: Core programming language.
- **CrewAI**: Agent-based AI framework for task automation.
- **Gradio**: Web-based UI for interactive user interaction.
- **Google Gemini Flash**: LLM used for text generation and processing.
- **Neo4J**: Graph database for retrieving company data.
- **Pandas** (optional): For data manipulation and analysis.

## Backend Configuration

### Prerequisites
1. Install `uv` if not already installed:
   ```bash
   pip install uv
   ```
2. Navigate to your project directory and install dependencies:
   ```bash
   crewai install
   ```
   (Optional: Lock dependencies using the CLI command.)

### Customization
1. Add environment variables to the `.env` file:
   ```plaintext
   MODEL=gemini/gemini-1.5-flash
   MODEL_API_KEY=<model_api_key> # Your API key here
   ```
   Generate a new API key for GEMINI model from the [AI Studio](https://aistudio.google.com/app/apikey) website.

2. Modify configuration files as needed:
   - `src/report_genie/config/agents.yaml`: Define your agents.
   - `src/report_genie/config/tasks.yaml`: Define your tasks.
   - `src/report_genie/crew.py`: Add custom logic, tools, and arguments.
   - `src/report_genie/main.py`: Customize inputs for agents and tasks.
   - `src/report_genie/app.py`: Configure Gradio app settings.

### Running the Backend
To start the backend server and execute tasks:
```bash
uv run report_genie
```
The Gradio interface will be available at `http://localhost:7860/`.

## Deployment
The app is deployed on Hugging Face Spaces. You can try it out [here](https://huggingface.co/spaces/deepakpant/report-genie).

## Additional Notes
- Ensure all environment variables are correctly set in the `.env` file.
- Regularly update your agents and tasks configuration to enhance functionality.
- Refer to the CrewAI documentation for advanced customizations.


The Gradio app allows users to interact with the backend and generate reports.

## Future Enhancements
- Support for multi-language reports.
- Integration with cloud storage.
- Export to additional formats like Excel, PPT, and JSON.

## License
MIT License

## Contributors
- Deepak Pant (@DeepakPant93)

## Contact
For any queries, reach out at [deepak.93p@gmail.com](mailto:deepak.93p@gmail.com).

## Support
 If you like my work and want to support give a ⭐ to the repo.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://buymeacoffee.com/deepakpant) 

Thank you so much ❤️.
