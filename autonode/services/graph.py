import json

from autonode.config.config import get_config
from autonode.factories.node_factory import NodeFactory


class Graph:
    def __init__(self, graph_path: str):
        self.graph_json = self._read_graph(graph_path)
        self.visited = set()
        self.node_factory = NodeFactory()
        self.graph_dict = self.build_graph_dict()

    def _read_graph(self, graph_path: str):
        with open(graph_path, "r") as graph_file:
            graph_json = json.load(graph_file)
        return graph_json

    def build_graph_dict(self) -> dict:
        graph_dict = {}
        for key, value in self.graph_json.items():
            value["id"] = key
            value['llm'] = get_config('GPT_4_0125_PREVIEW_VERSION')
            node = self.node_factory.create_node(
                **value
            )
            graph_dict[key] = node
            print(f"Graph - {graph_dict}")
        return graph_dict

    def __repr__(self):
        # print the graph_dict
        for key, value in self.graph_dict.items():
            print(f"{key}: {value.__repr__()}")
