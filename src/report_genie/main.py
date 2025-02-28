#!/usr/bin/env python
import sys
import warnings

from report_genie.crew import ExpresslyServer
import dotenv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

dotenv.load_dotenv()


def run():
    """
    Run the crew.
    """

    inputs = {
        "prompt": "I want to thanks DeepLearning and John from the crewAI for this amazing course..",
        "format": "Email",
        "tone": "Friendly",
        "target_audience": "",
    }

    ExpresslyServer().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        ExpresslyServer().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ExpresslyServer().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        ExpresslyServer().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
