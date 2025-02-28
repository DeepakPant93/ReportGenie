from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.llm import LLM
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from dotenv import load_dotenv
import os
from typing import Dict, Any, Optional
import json
from report_genie.utils.utils import load_json_data, sanitize_input

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

FORMAT_JSON_FILE = "format.json"
TONE_JSON_FILE = "tone.json"
TARGET_AUDIENCE_JSON_FILE = "target_audience.json"
CONTENT_STYLE_MAPPING_JSON_FILE = "content_style_mapping.json"
KNOWLEDGE_SOURCE_PATH = "knowledge"


@CrewBase
class ExpresslyServer:
    """ExpresslyServer crew"""

    # Create a knowledge source
    json_knowledge_source = JSONKnowledgeSource(
        file_paths=["format.json", "tone.json", "target_audience.json"],
    )

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = LLM(model=MODEL, api_key=GEMINI_API_KEY, temperature=0.7)

    @before_kickoff
    def validate_inputs(
        self, inputs: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Validate and process user inputs based on the active tab selection.

        This method checks the integrity and presence of required inputs, loads
        necessary JSON data, and validates the active_tab value to ensure the
        appropriate fields are populated. It formats the inputs for further processing.

        Parameters:
        inputs (Optional[Dict[str, Any]]): The dictionary containing user inputs,
        including 'target_audience', 'format', 'tone', 'active_tab', and 'prompt'.

        Returns:
        Optional[Dict[str, Any]]: A dictionary formatted with context, format, tone,
        and target_audience details based on the inputs provided.

        Raises:
        ValueError: If inputs are missing, not a dictionary, or required fields
        ('active_tab', 'prompt', 'format', 'tone', 'target_audience') are not provided
        or invalid.
        """

        if inputs is None or len(inputs) == 0 or not isinstance(inputs, dict):
            raise ValueError("Inputs is required and must be a dictionary")

        ## Get the first element from the list of inputs and get the value of target, format, active_tab and prompt
        query = inputs
        target_audience: str = sanitize_input(query.get("target_audience"))
        content_format: str = sanitize_input(query.get("format"))
        content_tone: str = sanitize_input(query.get("tone"))
        prompt: str = query.get("prompt")

        # Check if prompt are not None
        if prompt is None:
            raise ValueError("Prompt is required")

        # Load JSON data from content_style_mapping.json
        content_style_mapping_json = load_json_data(
            CONTENT_STYLE_MAPPING_JSON_FILE, KNOWLEDGE_SOURCE_PATH
        )
        tone_json = load_json_data(TONE_JSON_FILE, KNOWLEDGE_SOURCE_PATH)
        format_json = load_json_data(FORMAT_JSON_FILE, KNOWLEDGE_SOURCE_PATH)
        target_audience_json = load_json_data(
            TARGET_AUDIENCE_JSON_FILE, KNOWLEDGE_SOURCE_PATH
        )

        if target_audience != "":
            ## Resetting the format and tone as per the target audience
            mappings: dict = content_style_mapping_json.get("target_audience").get(
                target_audience
            )
            format_dict = format_json.get("format").get(mappings.get("format"))
            tone_dict = tone_json.get("tone").get(mappings.get("tone"))
            target_audience_dict = target_audience_json.get("target_audience").get(
                target_audience
            )
        elif content_format != "" and content_tone != "":
            ## Constructing a target_audience_dict with empty values and populating the format and tone as per the input
            target_audience_dict = {
                "name": "",
                "description": "",
                "ideal_audience": "",
            }
            format_dict = format_json.get("format").get(content_format)
            tone_dict = tone_json.get("tone").get(content_tone)
        else:
            raise ValueError("Provide either target audience or format and tone")

        ## Format the inputs
        inputs = {
            "context": prompt,
            "format": format_dict,
            "tone": tone_dict,
            "target_audience": target_audience_dict,
        }

        return inputs

    @agent
    def content_creator(self) -> Agent:
        """
        Initializes and returns an Agent for content creation.

        This agent is configured using predefined settings for the content creator
        and utilizes a language model (LLM) for generating content. The agent
        accesses a JSON knowledge source to enhance its capabilities and operates
        in verbose mode for detailed output logging.

        Returns:
            Agent: An initialized agent configured for content creation.
        """

        return Agent(
            config=self.agents_config["content_creator"],
            llm=self.llm,
            knowledge_source=[self.json_knowledge_source],
            verbose=True,
        )

    @task
    def content_creator_task(self) -> Task:
        """
        Initializes and returns a Task for content creation.

        This task is configured using predefined settings for content creation
        and is used by the content creator agent to generate content.

        Returns:
            Task: An initialized task configured for content creation.
        """
        return Task(
            config=self.tasks_config["content_creator_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExpresslyServer crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            knowledge_source=[self.json_knowledge_source],
            verbose=True,
        )
