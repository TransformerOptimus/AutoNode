from autonode.clients.http_client import HttpClient
from autonode.config.config import get_config


class YoloClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.http_client = HttpClient(base_url=get_config("YOLO_BASE_URL"))

    def detect(self, image_path: str):
        try:
            files = {'image': open(image_path, 'rb')}
            response = self.http_client.post_file(endpoint="/api/yolo/image/detect", files=files)

            if response["success"]:
                return response["result"]

        except Exception as e:
            raise e
