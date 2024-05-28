class ElementNotFoundException(Exception):
    def __init__(self, request_id, element):
        self.message = f"Element {element} not found for request_id: {request_id} after 5 retries."
        super().__init__(self.message)
