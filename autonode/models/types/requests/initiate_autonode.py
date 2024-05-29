from pydantic import BaseModel


class InitiateAutoNodeRequest(BaseModel):
    site_url: str
    objective: str
    graph_path: str
    planner_prompt: str
    # site_tree: str
