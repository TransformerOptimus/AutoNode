from abc import ABC, abstractmethod
from autonode.llms.base_llm import BaseLlm


class BaseAgent(ABC):
    _version = "v1"
    _type = "Default"

    @property
    def version(self):
        return self._version

    @property
    def type(self):
        return self._type

    def __init__(self, llm_instance: BaseLlm):
        self.llm = llm_instance

    @abstractmethod
    def execute(self):
        pass

    def get_prompt_file_path(self, prompt_file_path='', version='v1'):
        return f"agent/execution_agents/" + {self._type} + '/' + {version} + '/' + prompt_file_path