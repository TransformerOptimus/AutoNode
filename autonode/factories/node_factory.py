
class NodeFactory:
    _instance = None
    _registry = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register_node_type(cls, node_type):
        """
        A decorator to register node classes under a specific type.

        Args:
            node_type (str): Type of the node.

        Raises:
            ValueError: If the node type is already registered.
        """

        def decorator(node_class):
            if node_type in cls._registry:
                raise ValueError(f"Node type '{node_type}' is already registered.")
            cls._registry[node_type] = node_class
            return node_class

        return decorator

    @classmethod
    def create_node(cls, node_type, *args, **kwargs):
        """
        Creates an instance of a node based on its type with given arguments.

        Args:
            node_type (str): Type of the node.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Node: Instance of the created node.

        Raises:
            ValueError: If the node type is not registered.
        """
        node_class = cls._registry.get(node_type)
        print(f"REGISTRY - {cls._registry}")
        if not node_class:
            raise ValueError(f"Node type '{node_type}' is not registered.")
        # TODO: Sanity Check before creating the node. Check if all the required arguments are passed.
        return node_class(*args, **kwargs)


from autonode.nodes import *
