import json


def load_json_data(file_name: str, file_path: str) -> dict:
    """
    Loads JSON data from a file.

    Args:
        file_name (str): The name of the JSON file.
        file_path (str): The path to the directory containing the file.

    Returns:
        dict: The content of the JSON file as a dictionary.
    """

    file_path = f"{file_path}/{file_name}"
    with open(file_path, "r") as file:
        return json.load(file)


def sanitize_input(input: str) -> str:
    """
    Sanitizes a string by stripping, lower casing, and replacing whitespace and hyphens with underscores.

    Args:
        input (str): The string to be sanitized.

    Returns:
        str: The sanitized string.
    """
    if input is None or input == "":
        return ""
    return input.strip().lower().replace(" ", "_").replace("-", "_")
