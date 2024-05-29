import os
import random

from autonode.agents.planning_agent import PlanningAgent
from autonode.config.config import get_config
from autonode.llms.open_ai import OpenAi
from autonode.nodes.base_node import Node
from autonode.factories.node_factory import NodeFactory
from autonode.utils.exceptions.llm_objective_exception import LLMObjectiveException
from autonode.utils.helpers.prompt_helper import format_planning_prompt
from autonode.logger.logger import logger


@NodeFactory.register_node_type("planning")
class PlanningNode(Node):
    """Node for handling planning tasks."""

    def __init__(
        self,
        id: str,
        node_name: str,
        adjacent_from: list,
        adjacent_to: list,
        description: str,
        llm: str,
        planning_prompt: str,
        **kwargs
    ):
        """
        Args:
            id (str): Unique identifier for the node.
            node_name (str): Type of the node.
            adjacent_from (list): List of nodes that are adjacent to this node.
            adjacent_to (list): List of nodes that this node is adjacent to.
            description (str): Description of the node.
            llm (str): The instance of the LLM (Language Model) will be chosen from the LLM factory module.
            planning_prompt (str): Prompt for planning.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            id, node_name, adjacent_from, adjacent_to, description, llm, **kwargs
        )
        self.planning_prompt = planning_prompt
        self.llm_4o = OpenAi(api_key=os.getenv("OPENAI_API_KEY"),
                             model=get_config("GPT_4O_VERSION"),
                             temperature=random.uniform(0.0, 0.2),
                             top_p=random.uniform(0.9, 0.99),
                             presence_penalty=1,
                             frequency_penalty=1)

    def run(
        self,
        autonode_object,
        objective,
        db_session,
        request_id,
        prompt,
        llm_response,
        llm_instance,
        planner_prompt=None,
        **kwargs
    ):
        """
        Runs the planning node.

        Args:
            autonode_object: Object representing the autonode.
            objective: Objective of the planning.
            db_session: Database session object.
            request_id: ID of the request.
            prompt: Prompt for selecting the node.
            llm_response: LLM (Language Model) response for the prompt.
            llm_instance: Instance of the LLM (Language Model)
            planner_prompt: Which prompt to use
        """
        logger.info(f"Running Planning Node: {self.node_name} for request_id: {request_id}")
        planning_agent = PlanningAgent(llm_instance=self.llm_4o, planner_prompt=planner_prompt)
        autonode_object.objective = format_planning_prompt(planning_agent.execute(objective=objective))
        logger.info(f"Objective for the request_id: {request_id} is: {autonode_object.objective}")

        if autonode_object.objective is None:
            raise LLMObjectiveException(request_id=request_id)

        self.update_action_in_db(
            session=db_session, request_id=request_id, prompt=prompt, llm_response=llm_response
        )

    def update_action_in_db(self, session, request_id, prompt, llm_response):
        """
        Updates action in the database.

        Args:
            session: Database session object.
            request_id: ID of the request.
            prompt: Prompt for selecting the node.
            llm_response: LLM (Language Model) response for the prompt.
        """
        pass

    def actions_taken(self):
        """Returns actions taken by the node."""
        return ""

    def __repr__(self):
        """Representation of the PlanningNode."""
        return f"PlanningNode({self.id}, {self.node_name}, {self.description})"
