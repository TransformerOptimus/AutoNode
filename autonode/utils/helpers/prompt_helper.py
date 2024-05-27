from autonode.config.settings import Settings
import re


config = Settings()


def format_planning_prompt(objective: str):
    """
    Extracts the relevant part of the planning prompt based on specific delimiters.
    Args:
        objective (str): The input string containing the planning objective with potential delimiters.
    Returns:
        str or None: The extracted part of the objective following a recognized delimiter, or None if no delimiter is found.
    """
    print(f"Planning Objective: {objective}")
    delimiters = ['!@#delim#@!', 'proceed:', 'ACTIONS::']
    for delimiter in delimiters:
        pattern = rf"(?<={re.escape(delimiter)})(.*)"
        match = re.search(pattern, objective, flags=re.DOTALL)
        if match:
            return match.group(1).strip()
    return None
