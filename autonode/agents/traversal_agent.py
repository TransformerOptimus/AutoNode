import jellyfish
import ast
from autonode.agents.base_agent import BaseAgent
from autonode.llms.base_llm import BaseLlm
from autonode.logger.logger import logger
from autonode.utils.helpers.cleanup_helper import CleanupHelper
from autonode.prompts.openai_prompt import NODE_SELECTION_PROMPT
from autonode.utils.decorators.retry_decorator import retry


class TraversalAgent(BaseAgent):

    def __init__(self, llm_instance: BaseLlm):
        super().__init__(llm_instance)

    def execute(self, objective, actions_taken, graph_node, graph_dict=None, threshold_similarity=0.70):
        """
        Traverse to the next node based on the response from the ask_which_node_to_select function.
        """
        if graph_dict is None:
            graph_dict = {}

        for depth in range(5):
            logger.info(f"Traversing to the next node at depth: {depth}")
            try:
                node_to_select, prompt, response = self.ask_which_node_to_select(
                    objective=objective,
                    actions=actions_taken,
                    parent_node=graph_node,
                    graph_dict=graph_dict
                )
                logger.info(f"Reasoning on selection of node: {node_to_select['option']}")

                return_node = self.find_most_similar_node(node_to_select, graph_node, graph_dict, threshold_similarity)
                if return_node:
                    return return_node, prompt, response

            except Exception as e:
                logger.error(f"Error while running Traversal Agent: {e}")
                continue

        raise Exception("Depth exceeded, can't find the next node")

    def find_most_similar_node(self, node_to_select, graph_node, graph_dict, threshold_similarity):
        highest_similarity, return_node = -10, None

        for child_id in graph_node.adjacent_to:
            child_node = graph_dict.get(str(child_id))
            if child_node:
                similarity = jellyfish.jaro_winkler_similarity(child_node.node_name, node_to_select["option"])
                if similarity > highest_similarity:
                    highest_similarity, return_node = similarity, child_node

        if highest_similarity > threshold_similarity:
            return return_node

        raise Exception(f"No suitable node found for the option: {node_to_select['option']} with similarity threshold: {threshold_similarity}")

    def ask_which_node_to_select(self, objective, actions, parent_node, graph_dict=None):
        options = ""
        for idx, children_node in enumerate(parent_node.adjacent_to):
            child = graph_dict[str(children_node)]
            if child.type_description:
                options += (f"{idx + 1}. {child.node_name}  Description: {child.description}"
                            f" Type Description: {child.type_description}\n")
            else:
                options += f"{idx + 1}. {child.node_name}  Description: {child.description} \n"

        prompt = NODE_SELECTION_PROMPT.format(objective=objective, actions=actions, options=options)
        messages = [{"role": "user", "content": prompt}]
        return self.query_llm(messages=messages, prompt=prompt)

    @retry(max_attempts=3, backoff=2, exceptions=Exception)
    def query_llm(self, messages, prompt):
        response = self.llm.chat_completion(messages=messages)
        content = response["content"]
        content = CleanupHelper.clean_response(response=content)

        content_object = ast.literal_eval(content)
        return content_object, prompt, content
