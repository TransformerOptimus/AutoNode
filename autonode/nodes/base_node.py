from abc import ABC, abstractmethod

from autonode.llms.base_llm import BaseLlm


class Node(ABC):
    """Base Node class for each node in the graph."""

    def __init__(
            self,
            id: str,
            node_name: str,
            adjacent_from: list,
            adjacent_to: list,
            description: str,
            llm: str,
            **kwargs,
    ):
        """
        Args:
            id (str): Unique identifier for the node.
            node_name (str): Type of the node.
            adjacent_from (list): List of nodes that are adjacent to this node.
            adjacent_to (list): List of nodes that this node is adjacent to.
            description (str): Description of the node.
            llm (str): The instance of the LLM (Language Model) will be chosen from the LLM factory module.
            **kwargs: Additional keyword arguments.
        """
        self.id = id
        self.node_name = node_name
        self.adjacent_from = adjacent_from
        self.adjacent_to = adjacent_to
        self.description = description
        self.llm = llm
        self.output = None
        self.token_counter = 0
        self.__dict__.update(kwargs)

    @abstractmethod
    def run(self, **kwargs):
        """Runs the capability of the node."""
        raise NotImplementedError

    @abstractmethod
    def update_action_in_db(self, **kwargs):
        """Updates action in the database."""
        raise NotImplementedError

    @abstractmethod
    def actions_taken(self):
        """Actions taken by the node."""
        raise NotImplementedError

    def get_output(self, **kwargs):
        """Gets the output of the node."""
        return self.output

    def get_dependencies(self):
        """Gets dependencies of the node."""
        return self.adjacent_from

    def get_children(self):
        """Gets children of the node."""
        return self.adjacent_to

    def has_next_node(self) -> bool:
        """Checks if the node has next nodes."""
        return bool(self.adjacent_to)

    def __repr__(self):
        """Representation of the node."""
        return f"Node({self.id}, {self.node_name}, {self.description})"
