import time
from autonode.logger.logger import logger
from autonode.models.actions import Actions
from autonode.nodes.base_node import Node
from autonode.factories.node_factory import NodeFactory


@NodeFactory.register_node_type("navigation")
class Navigation(Node):
    """Node for Navigation to a different URL

    Args:
        id (str): Unique identifier for the node
        node_name (str): Name of the node
        node_type (str): Type of the node
        adjacent_from (list): List of nodes that are adjacent to this node
        adjacent_to (list): List of nodes that this node is adjacent to
        llm (str): The instance of the llm will be chosen from the llm factory module
        url (str): URL to navigate to
    """

    def __init__(self, id: str, node_name: str, adjacent_from: list, adjacent_to: list, description: str, llm: str,
                 url: str, **kwargs):
        super().__init__(id, node_name, adjacent_from, adjacent_to, description, llm, **kwargs)
        self.loop = None
        self.url = url

    def run(self, autonode_object, steps, history, objective, web_automater, db_session, s3_client, request_id, request_dir,
            prompt, llm_response, loop,
            previous_node,
            **kwargs,
    ):
        self.loop = loop
        time.sleep(5)
        self.loop.run_until_complete(web_automater.navigate_page(self.url))
        logger.info(f"Navigation to {self.url} completed")

        self.update_action_in_db(
            db_session, request_id, prompt, llm_response
        )

    def actions_taken(self):
        return f"Navigation to {self.url}"

    def update_action_in_db(self, session, request_id, prompt, llm_response):
        Actions.add_action_taken(
            session=session,
            request_id=request_id,
            screenshot_id=None,
            prompt=prompt,
            llm_response=llm_response,
            action=f"Navigation to {self.url}",
            node_id=self.id,
            text="",
        )

    def __repr__(self):
        return f"NavigationNode({self.id}, {self.node_name}, {self.description})"
