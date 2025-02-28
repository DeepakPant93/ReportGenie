from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.llm import LLM
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from dotenv import load_dotenv
import os
from typing import Dict, Any, Optional
import json
from report_genie.utils.utils import load_json_data, sanitize_input
from report_genie.tools.neo4j_tools import get_city_info, get_news

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

FORMAT_JSON_FILE = "format.json"
TONE_JSON_FILE = "tone.json"
TARGET_AUDIENCE_JSON_FILE = "target_audience.json"
CONTENT_STYLE_MAPPING_JSON_FILE = "content_style_mapping.json"
KNOWLEDGE_SOURCE_PATH = "knowledge"


@CrewBase
class ReportGenieServer:
    """ExpresslyServer crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = LLM(model=MODEL, api_key=GEMINI_API_KEY, temperature=0.7)

    @agent
    def data_researcher(self) -> Agent:
        """
        The data_researcher agent is responsible for fetching data from the given data sources.
        It takes the data sources as input and returns the data as JSON.
        """
        return Agent(
            config=self.agents_config["data_researcher"],
            llm=self.llm,
            tools=[get_city_info],
            verbose=True,
        )

    @agent
    def news_analyst(self) -> Agent:
        """
        The news_analyst agent is responsible for analyzing news articles
        related to the data fetched by the data_researcher agent.
        It takes the data sources as input and returns a JSON object
        containing the analysis results.
        """
        return Agent(
            config=self.agents_config["news_analyst"],
            llm=self.llm,
            tools=[get_news],
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        """
        The report_writer agent is responsible for generating a report given the
        results from the data_researcher and news_analyst agents.
        It takes the results from the agents as input and returns a JSON object
        containing the report.
        """
        return Agent(
            config=self.agents_config["report_writer"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def city_research_task(self) -> Task:
        """
        The city_research_task task is responsible for executing the data_researcher
        and news_analyst agents in order.
        It takes no input and returns a JSON object containing the results of the
        agents.
        """
        return Task(
            config=self.tasks_config["city_research_task"],
        )

    @task
    def news_analysis_task(self) -> Task:
        """
        The news_analysis_task task is responsible for executing the news_analyst
        agent to analyze news articles related to the data fetched by the
        data_researcher agent.
        It takes no input and returns a JSON object containing the analysis results.
        """
        return Task(
            config=self.tasks_config["news_analysis_task"],
            context=[self.city_research_task()],
        )

    @task
    def report_writing_task(self) -> Task:
        """
        The report_writing_task task is responsible for executing the report_writer
        agent to generate a report based on the findings from previous tasks.
        It takes no input and returns a JSON object containing the generated report.
        """

        return Task(
            config=self.tasks_config["report_writing_task"],
            context=[self.city_research_task(), self.news_analysis_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExpresslyServer crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
