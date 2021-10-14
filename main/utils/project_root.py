from pathlib import Path


def get_project_root() -> Path:
    """
    Return the root of the project (outside main) where the Pipfile and Readme resides
    """
    return Path(__file__).parent.parent.parent


def get_useragents_json() -> Path:
    return get_project_root().joinpath('user_agents.json')

