from abc import ABC, abstractmethod


class BaseLlm(ABC):
    def __init__(self):
        self.encoding = None

    @abstractmethod
    def chat_completion(self, messages, **kwargs):
        pass

    @abstractmethod
    def get_model(self):
        pass
