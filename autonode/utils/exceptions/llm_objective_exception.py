class LLMObjectiveException(Exception):
    def __init__(self, request_id):
        self.message = f"Received Null Objective from llm for request_id: {request_id}."
        super().__init__(self.message)
        